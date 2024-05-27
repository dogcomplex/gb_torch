import torch
import numpy as np
import threading
import time
from opcodes import EmulatorOpcodes
from memory_bank import NoMBC, MBC1, MBC2, MBC3, MBC5

# Simplified ASCII characters for representing different pixel intensities
ASCII_PIXELS = [' ', '░', '▒', '▓']

class GameBoyEmulator:
    
    def __init__(self, rom_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.rom_path = rom_path
        self.rom_data = self.load_rom(rom_path)
        self.memory = self.initialize_memory()
        self.setup_memory_controller()  # Setup the memory controller based on the cartridge type
        self.registers = self.initialize_registers()
        self.flags = {'Z': 0, 'N': 0, 'H': 0, 'C': 0}  # Flag registers
        self.gpu_state = self.initialize_gpu_state()
        self.running = True
        self.input_register = 0xFF  # All buttons unpressed (buttons are active low)
        self.parse_header()
        torch.cuda.init()
        
        self.opcodes = EmulatorOpcodes(self)
        self.opcode_map = self.opcodes.create_opcode_map()
        self.lock = threading.Lock()  # Add a lock for thread safety

    def initialize_registers(self):
        """ Initialize registers to post-BIOS values. """
        # Example values: A=0x01, F=0xB0, B=0x00, C=0x13, D=0x00, E=0xD8, H=0x01, L=0x4D, SP=0xFFFE, PC=0x0100
        # Adjust according to Game Boy CPU specification
        return torch.tensor([0x01, 0xB0, 0x00, 0x13, 0x00, 0xD8, 0x01, 0x4D, 0xFFFE, 0x0100], dtype=torch.int32, device=self.device)


    def load_rom(self, file_path):
        """
        Loads the ROM from the specified file path into a tensor.
        Ensures the data is writable by copying it from the buffer.
        """
        with open(file_path, "rb") as f:
            # Create a writable copy of the data read from the file.
            rom_data = np.frombuffer(f.read(), dtype=np.uint8).copy()
        # Convert the writable numpy array to a PyTorch tensor and pin memory for faster transfer if needed.
        rom_tensor = torch.from_numpy(rom_data)  # Now this should not raise a warning
        rom_tensor = rom_tensor.pin_memory()  # Pin memory to prepare for possible transfer to GPU
        return rom_tensor.to(self.device, non_blocking=True)

    def parse_header(self):
        """
        Parses the ROM header to get metadata and set up memory banking if required.
        Extracts the title from the ROM data tensor and decodes it from ASCII.
        """
        # Extract the title slice from the tensor and convert it to bytes
        title_bytes = self.rom_data[0x0134:0x0143].cpu().numpy().tobytes()
        title = title_bytes.decode('ascii').strip()
        # Similarly, get the cartridge type from the tensor
        cartridge_type = self.rom_data[0x0147].item()  # Use .item() to get a Python scalar from a tensor
        print(f"Loaded Game: {title}, Cartridge Type: {cartridge_type}")


    def setup_memory_controller(self):
        cartridge_type = self.rom_data[0x0147].item()
        rom_size = len(self.rom_data)
        # Assuming a fixed RAM size, adjust as necessary
        ram_size = 32 * 1024  # Example: 32KB RAM

        if cartridge_type == 0x00:
            self.memory_controller = NoMBC(self.memory, rom_size, ram_size)
        elif cartridge_type in [0x01, 0x02, 0x03]:
            self.memory_controller = MBC1(self.memory, rom_size, ram_size)
        elif cartridge_type in [0x05, 0x06]:
            self.memory_controller = MBC2(self.memory, rom_size, ram_size)
        elif cartridge_type in [0x0F, 0x10, 0x11, 0x12, 0x13]:
            self.memory_controller = MBC3(self.memory, rom_size, ram_size)
        elif cartridge_type in [0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E]:
            self.memory_controller = MBC5(self.memory, rom_size, ram_size)
        else:
            raise ValueError("Unsupported cartridge type")
        
        print(f"Memory Controller initialized for Cartridge Type: {hex(cartridge_type)}")


    def initialize_gpu_state(self):
        """
        Initializes and returns a state necessary for GPU operations.
        Placeholder for more complex GPU state configurations.
        """
        return {}

    def initialize_memory(self):
        """
        Initializes the emulator's memory structure using tensors for efficient GPU access.
        Adjust the memory size if the ROM size exceeds standard Game Boy memory.
        """
        rom_size = len(self.rom_data)
        memory_size = max(65536, rom_size)  # Ensure at least the standard Game Boy memory size
        memory = torch.zeros(memory_size, dtype=torch.uint8, device=self.device)
        memory[:rom_size] = self.rom_data  # Load ROM data into memory
        return memory

    def fetch_instruction(self):
        pc = self.registers[9].item()  # Program counter index is 9
        if pc >= len(self.memory):
            print(f"Program Counter out of memory bounds: {pc}")
            self.stop()
            return 0  # NOP opcode to safely handle out-of-bounds without crashing
        instruction = self.memory[pc].item()
        # print(f"Fetched opcode {instruction:X} from address {pc:X}")
        # test if opcode found in opcode_map
        if instruction not in self.opcode_map:
            print(f"Unknown opcode: {instruction:X}")
            self.stop()
            return 0
        self.registers[9] += 1  # Increment the program counter
        return instruction

    
    def read_memory(self, address):
        if address == 0xFF00:
            return self.get_input_state()
        if address < 0x8000:  # ROM area
            return self.memory_controller.read(address)
        # Add other memory areas handling
        return self.memory[address]
    
    def get_input_state(self):
        # Return the current state of the input register
        return self.input_register
    
    def update_input_state(self, button, pressed):
        """
        Update the input state for a given button.
        `button` should be one of 'start', 'select', 'a', 'b', 'up', 'down', 'left', 'right'
        `pressed` is a boolean, where True means the button is pressed.
        """
        button_map = {
            'start': 0x7,
            'select': 0x6,
            'b': 0x5,
            'a': 0x4,
            'down': 0x3,
            'up': 0x2,
            'left': 0x1,
            'right': 0x0
        }
        if button in button_map:
            if pressed:
                self.input_register &= ~(1 << button_map[button])  # Set bit to 0 to indicate pressed
            else:
                self.input_register |= (1 << button_map[button])  # Set bit to 1 to indicate released


    def write_memory(self, address, value):
        if address < 0x8000:  # ROM bank switching area
            self.memory_controller.write(address, value)
            return
        # Handle RAM enable and writing to RAM area
        self.memory[address] = value


    def decode_execute(self, opcode):
        if opcode is None:
            print("Error: Fetched None as opcode")
            self.stop()
            exit(1)
            #return
        if opcode in self.opcode_map:
            self.opcode_map[opcode]()
        else:
            print(f"Unknown opcode: {opcode:X}")
            self.stop()
            exit(1)

    def main_emulation_loop(self):
        try:
            while self.running:
                with self.lock:  # Ensure thread safety
                    opcode = self.fetch_instruction()
                    self.decode_execute(opcode)
                    # time.sleep(0.1)  # You may adjust or remove the sleep time as needed
        except KeyboardInterrupt:
            self.stop()

    def extract_tile_data(self, tile_index):
        """
        Extracts tile data for the given tile index from the VRAM.
        Each tile is 16 bytes long, and each byte represents a row of the tile.
        """
        tile_address = 0x8000 + (tile_index * 16)
        tile_data = self.memory[tile_address:tile_address + 16]
        return tile_data.cpu().numpy()

    def render_tile(self, tile_data):
        """
        Renders a single tile (8x8 pixels) as a single ASCII character for each 4x4 block of pixels.
        """
        ascii_tile = [[' ' for _ in range(2)] for _ in range(2)]
        for row in range(0, 8, 4):
            for col in range(0, 8, 4):
                block_intensity = 0
                for sub_row in range(4):
                    byte1 = tile_data[row + sub_row]
                    byte2 = tile_data[row + sub_row + 1]
                    for bit in range(7, 3, -1):
                        pixel = ((byte1 >> bit) & 1) | (((byte2 >> bit) & 1) << 1)
                        block_intensity += pixel
                block_intensity //= 16  # Average intensity over the 4x4 block
                ascii_tile[row // 4][col // 4] = ASCII_PIXELS[block_intensity]
        return ascii_tile
    
    def render_screen(self):
        try:
            screen = [['-' for _ in range(20 * 2)]]
            screen += [[' ' for _ in range(20 * 2)] for _ in range(18 * 2)]
            for tile_y in range(18):
                for tile_x in range(20):
                    # Safely calculate the index in the tile map
                    tile_map_index = 0x9800 + (tile_y * 32) + tile_x
                    if tile_map_index >= len(self.memory):
                        continue  # Skip if out of bounds
                    tile_index = self.memory[tile_map_index].item()
                    if tile_index is None:
                        continue  # Skip if tile index is None
                    tile_data = self.extract_tile_data(tile_index)
                    ascii_tile = self.render_tile(tile_data)
                    for row in range(2):
                        for col in range(2):
                            screen[tile_y * 2 + row][tile_x * 2 + col] = ascii_tile[row][col]
            return '\n'.join([''.join(row) for row in screen])
        except Exception as e:
            print(f"Error while rendering screen: {str(e)}")
            self.stop()
            return "Error in rendering"
        
    def update_gui(self):
        try:
            while self.running:
                with self.lock:
                    #print(f"\033[H\033[J{self.render_screen()}")  # Clear screen and render
                    print(f"Registers: {self.registers}")
                    print(f"Flags: {self.flags}")
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """ Signal all threads to stop. """
        self.running = False

    def text_gui(self):
        emulation_thread = threading.Thread(target=self.main_emulation_loop)
        gui_update_thread = threading.Thread(target=self.update_gui)

        # Start threads
        emulation_thread.start()
        gui_update_thread.start()

        try:
            while True:
                command = input("Enter command (button_down, button_up, pause, resume, quit): ").strip().lower()
                if command.startswith('button_down'):
                    _, button = command.split()
                    self.update_input_state(button, True)
                elif command.startswith('button_up'):
                    _, button = command.split()
                    self.update_input_state(button, False)
                elif command == "quit":
                    self.stop()
                    emulation_thread.join()
                    gui_update_thread.join()
                    break
                elif command == "pause":
                    self.running = False
                elif command == "resume":
                    self.running = True
                    if not emulation_thread.is_alive():
                        emulation_thread = threading.Thread(target=self.main_emulation_loop)
                        emulation_thread.start()
                    self.running = True
                    if not emulation_thread.is_alive():
                        emulation_thread = threading.Thread(target=self.main_emulation_loop)
                        emulation_thread.start()
        except KeyboardInterrupt:
            self.stop()
            emulation_thread.join()
            gui_update_thread.join()

    def gui_test(self):
        """ Function to test the visual memory by running an animation loop with opcodes. """
        self.running = True

        # Fill some initial tile data in VRAM for testing
        for i in range(256):
            tile_address = 0x8000 + (i * 16)
            self.memory[tile_address:tile_address + 16] = torch.randint(0, 256, (16,), dtype=torch.uint8, device=self.device)
        
        def modify_vram():
            """ Modify VRAM to flip a tile for testing. """
            tile_address = 0x8000
            for i in range(16):
                self.memory[tile_address + i] = 255 - self.memory[tile_address + i]  # Invert the pixel data
        
        def animation_loop():
            """ Loop to perform VRAM modifications and update the screen. """
            try:
                count = 0
                while self.running and count < 20:  # Run for a limited number of iterations for testing
                    with self.lock:
                        modify_vram()
                        print(f"\033[H\033[J{self.render_screen()}")  # Clear screen and render
                        print(f"Registers: {self.registers}")
                        print(f"Flags: {self.flags}")
                    time.sleep(0.5)
                    count += 1
            except KeyboardInterrupt:
                self.stop()

        # Run the animation loop in the main thread
        animation_loop()

# Example usage
if __name__ == "__main__":
    emulator = GameBoyEmulator("path_to_your_rom.gb")
    emulator.text_gui()
