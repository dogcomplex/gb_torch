
class NoMBC:
    def __init__(self, memory, rom_size, ram_size):
        self.memory = memory

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value

class MBC1:
    #placeholder
    def __init__(self, memory, rom_size, ram_size):
        self.memory = memory
        self.rom_bank = 1

    def read(self, address):
        # MBC1 read logic based on current ROM bank
        pass

    def write(self, address, value):
        # MBC1 write logic for bank switching
        pass


class MBC2:
    #placeholder
    def __init__(self, memory, rom_size, ram_size):
        self.memory = memory
        self.rom_bank = 1

    def read(self, address):
        # MBC1 read logic based on current ROM bank
        pass

    def write(self, address, value):
        # MBC1 write logic for bank switching
        pass

class MBC3:
    def __init__(self, memory, rom_size, ram_size):
        self.memory = memory
        self.rom_size = rom_size
        self.ram_size = ram_size
        self.rom_bank = 1  # Starts from 1 because bank 0 is always loaded at 0x0000-0x3FFF
        self.ram_bank = 0  # Can be 0-3 for RAM banking or 0x08-0x0C for RTC registers
        self.ram_enable = False
        self.rtc_enabled = False
        self.latch_data = 0

    def read(self, address):
        data = self.memory[address]
        print(f"Read from {address:X}: {data}")
        if 0x0000 <= address < 0x4000:
            # Always read from ROM bank 0
            return self.memory[address]
        elif 0x4000 <= address < 0x8000:
            # Read from selected ROM bank
            rom_address = (self.rom_bank - 1) * 0x4000 + (address - 0x4000)
            return self.memory[rom_address]
        elif 0xA000 <= address < 0xC000:
            # Read from RAM bank, if enabled
            if self.ram_enable and not self.rtc_enabled:
                ram_address = self.ram_bank * 0x2000 + (address - 0xA000)
                return self.memory[ram_address]
            elif self.rtc_enabled:
                # Here would be RTC handling logic
                return 0  # Placeholder for RTC register
            else:
                return 0xFF  # Return 0xFF if RAM is not enabled

        return 0xFF

    def write(self, address, value):
        print(f"Write to {address:X}: {value}")
        if 0x0000 <= address < 0x2000:
            # Enable or disable RAM/RTC
            self.ram_enable = (value & 0x0F) == 0x0A
        elif 0x2000 <= address < 0x4000:
            # Select ROM bank (lower 7 bits)
            if value == 0:
                value = 1
            self.rom_bank = value & 0x7F
        elif 0x4000 <= address < 0x6000:
            # Select RAM bank or RTC register
            if 0 <= value <= 3:
                self.ram_bank = value
                self.rtc_enabled = False
            elif 0x08 <= value <= 0x0C:
                self.rtc_enabled = True
                # self.ram_bank could be set to RTC register index here
        elif 0x6000 <= address < 0x8000:
            # Latch clock data
            if self.latch_data == 0 and value == 1:
                # Latch clock data logic here
                pass
            self.latch_data = value

    def get_current_rom_bank(self):
        return self.rom_bank

    def get_current_ram_bank(self):
        return self.ram_bank


class MBC5:
    def __init__(self, memory, rom_size, ram_size):
        self.memory = memory
        self.rom_size = rom_size
        self.ram_size = ram_size
        self.rom_bank = 1  # Default ROM bank starts at 1 since 0 is always loaded
        self.ram_bank = 0
        self.ram_enable = False

    def read(self, address):
        if address < 0x4000:
            # Always read from bank 0
            return self.memory[address]
        elif address >= 0x4000 and address < 0x8000:
            # Read from the selected ROM bank
            rom_address = address - 0x4000 + (self.rom_bank * 0x4000)
            return self.memory[rom_address]
        elif address >= 0xA000 and address < 0xC000:
            # Read from the selected RAM bank, if enabled
            if self.ram_enable and self.ram_size > 0:
                ram_address = address - 0xA000 + (self.ram_bank * 0x2000)
                return self.memory[ram_address]
            else:
                return 0xFF
        return 0xFF

    def write(self, address, value):
        if address < 0x2000:
            # Enable or disable RAM
            self.ram_enable = (value & 0x0F) == 0x0A
        elif address >= 0x2000 and address < 0x3000:
            # Write lower 8 bits of ROM bank number
            self.rom_bank = (self.rom_bank & 0x100) | value
            self.rom_bank &= (self.rom_size // 0x4000) - 1  # Mask ROM bank to valid range
        elif address >= 0x3000 and address < 0x4000:
            # Write the 9th bit of ROM bank number
            self.rom_bank = (self.rom_bank & 0xFF) | ((value & 0x01) << 8)
            self.rom_bank &= (self.rom_size // 0x4000) - 1  # Mask ROM bank to valid range
        elif address >= 0x4000 and address < 0x6000:
            # Write RAM bank number
            self.ram_bank = value & 0x0F
            self.ram_bank &= (self.ram_size // 0x2000) - 1  # Mask RAM bank to valid range
        elif address >= 0x6000 and address < 0x8000:
            # This range is typically used for clock control in MBC3, but not used in MBC5
            pass

    def get_current_rom_bank(self):
        return self.rom_bank

    def get_current_ram_bank(self):
        return self.ram_bank
