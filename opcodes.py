from functools import partial

class EmulatorOpcodes:
    def __init__(self, emulator):
        self.emulator = emulator

    def create_opcode_map(self):
        return {
            0x00: self.execute_NOP,
            0x01: partial(self.execute_LD_rr_nn, r1_index=1, r2_index=2),  # LD BC, nn
            0x02: partial(self.execute_LD_indirect_A, address_reg=1),  # LD (BC), A
            0x03: partial(self.execute_INC_rr, r1_index=1, r2_index=2),  # INC BC
            0x04: partial(self.execute_INC_r, r_index=1),  # INC B
            0x05: partial(self.execute_DEC_r, r_index=1),  # DEC B
            0x06: partial(self.execute_LD_r_n, r_index=1),  # LD B, n
            0x07: self.execute_RLCA,
            0x08: self.execute_LD_nn_SP,  # LD (nn), SP
            0x09: partial(self.execute_ADD_HL_rr, r1_index=1, r2_index=2),  # ADD HL, BC
            0x0A: partial(self.execute_LD_A_indirect, address_reg=1),  # LD A, (BC)
            0x0B: partial(self.execute_DEC_rr, r1_index=1, r2_index=2),  # DEC BC
            0x0C: partial(self.execute_INC_r, r_index=2),  # INC C
            0x0D: partial(self.execute_DEC_r, r_index=2),  # DEC C
            0x0E: partial(self.execute_LD_r_n, r_index=2),  # LD C, n
            0x0F: self.execute_RRCA,
            0x10: self.execute_STOP,
            0x11: partial(self.execute_LD_rr_nn, r1_index=3, r2_index=4),  # LD DE, nn
            0x12: partial(self.execute_LD_indirect_A, address_reg=3),  # LD (DE), A
            0x13: partial(self.execute_INC_rr, r1_index=3, r2_index=4),  # INC DE
            0x14: partial(self.execute_INC_r, r_index=3),  # INC D
            0x15: partial(self.execute_DEC_r, r_index=3),  # DEC D
            0x16: partial(self.execute_LD_r_n, r_index=3),  # LD D, n
            0x17: self.execute_RLA,
            0x18: self.execute_JR,  # JR n
            0x19: partial(self.execute_ADD_HL_rr, r1_index=3, r2_index=4),  # ADD HL, DE
            0x1A: partial(self.execute_LD_A_indirect, address_reg=3),  # LD A, (DE)
            0x1B: partial(self.execute_DEC_rr, r1_index=3, r2_index=4),  # DEC DE
            0x1C: partial(self.execute_INC_r, r_index=4),  # INC E
            0x1D: partial(self.execute_DEC_r, r_index=4),  # DEC E
            0x1E: partial(self.execute_LD_r_n, r_index=4),  # LD E, n
            0x1F: self.execute_RRA,
            0x20: partial(self.execute_JR_cc, condition='NZ'),  # JR NZ, n
            0x21: partial(self.execute_LD_rr_nn, r1_index=6, r2_index=7),  # LD HL, nn
            0x22: self.execute_LDI_HL_A,  # LDI (HL), A
            0x23: partial(self.execute_INC_rr, r1_index=6, r2_index=7),  # INC HL
            0x24: partial(self.execute_INC_r, r_index=6),  # INC H
            0x25: partial(self.execute_DEC_r, r_index=6),  # DEC H
            0x26: partial(self.execute_LD_r_n, r_index=6),  # LD H, n
            0x28: partial(self.execute_JR_cc, condition='Z'),  # JR Z, n
            0x29: partial(self.execute_ADD_HL_rr, r1_index=6, r2_index=7),  # ADD HL, HL
            0x2A: self.execute_LDI_A_HL,  # LDI A, (HL)
            0x2B: partial(self.execute_DEC_rr, r1_index=6, r2_index=7),  # DEC HL
            0x2C: partial(self.execute_INC_r, r_index=7),  # INC L
            0x2D: partial(self.execute_DEC_r, r_index=7),  # DEC L
            0x2E: partial(self.execute_LD_r_n, r_index=7),  # LD L, n
            0x2F: self.execute_CPL,  # CPL
            0x30: partial(self.execute_JR_cc, condition='NC'),  # JR NC, n
            0x31: self.execute_LD_SP_nn,  # LD SP, nn
            0x32: self.execute_LDD_HL_A,  # LDD (HL), A
            0x33: self.execute_INC_SP,  # INC SP
            0x34: self.execute_INC_HL,  # INC (HL)
            0x35: self.execute_DEC_HL,  # DEC (HL)
            0x36: self.execute_LD_HL_n,  # LD (HL), n
            0x38: partial(self.execute_JR_cc, condition='C'),  # JR C, n
            0x39: partial(self.execute_ADD_HL_rr, r1_index=8, r2_index=8),  # ADD HL, SP
            0x3A: self.execute_LDD_A_HL,  # LDD A, (HL)
            0x3B: self.execute_DEC_SP,  # DEC SP
            0x3C: partial(self.execute_INC_r, r_index=0),  # INC A
            0x3D: partial(self.execute_DEC_r, r_index=0),  # DEC A
            0x3E: self.execute_LD_A_n,  # LD A, n
            0x3F: self.execute_CCF,  # CCF
            0x40: partial(self.execute_LD_r_r, r1_index=1, r2_index=1),  # LD B, B
            0x41: partial(self.execute_LD_r_r, r1_index=1, r2_index=2),  # LD B, C
            0x42: partial(self.execute_LD_r_r, r1_index=1, r2_index=3),  # LD B, D
            0x43: partial(self.execute_LD_r_r, r1_index=1, r2_index=4),  # LD B, E
            0x44: partial(self.execute_LD_r_r, r1_index=1, r2_index=6),  # LD B, H
            0x45: partial(self.execute_LD_r_r, r1_index=1, r2_index=7),  # LD B, L
            0x46: partial(self.execute_LD_r_HL, r_index=1),  # LD B, (HL)
            0x47: partial(self.execute_LD_r_r, r1_index=1, r2_index=0),  # LD B, A
            0x48: partial(self.execute_LD_r_r, r1_index=2, r2_index=1),  # LD C, B
            0x49: partial(self.execute_LD_r_r, r1_index=2, r2_index=2),  # LD C, C
            0x4A: partial(self.execute_LD_r_r, r1_index=2, r2_index=3),  # LD C, D
            0x4B: partial(self.execute_LD_r_r, r1_index=2, r2_index=4),  # LD C, E
            0x4C: partial(self.execute_LD_r_r, r1_index=2, r2_index=6),  # LD C, H
            0x4D: partial(self.execute_LD_r_r, r1_index=2, r2_index=7),  # LD C, L
            0x4E: partial(self.execute_LD_r_HL, r_index=2),  # LD C, (HL)
            0x4F: partial(self.execute_LD_r_r, r1_index=2, r2_index=0),  # LD C, A
            0x50: partial(self.execute_LD_r_r, r1_index=3, r2_index=1),  # LD D, B
            0x51: partial(self.execute_LD_r_r, r1_index=3, r2_index=2),  # LD D, C
            0x52: partial(self.execute_LD_r_r, r1_index=3, r2_index=3),  # LD D, D
            0x53: partial(self.execute_LD_r_r, r1_index=3, r2_index=4),  # LD D, E
            0x54: partial(self.execute_LD_r_r, r1_index=3, r2_index=6),  # LD D, H
            0x55: partial(self.execute_LD_r_r, r1_index=3, r2_index=7),  # LD D, L
            0x56: partial(self.execute_LD_r_HL, r_index=3),  # LD D, (HL)
            0x57: partial(self.execute_LD_r_r, r1_index=3, r2_index=0),  # LD D, A
            0x58: partial(self.execute_LD_r_r, r1_index=4, r2_index=1),  # LD E, B
            0x59: partial(self.execute_LD_r_r, r1_index=4, r2_index=2),  # LD E, C
            0x5A: partial(self.execute_LD_r_r, r1_index=4, r2_index=3),  # LD E, D
            0x5B: partial(self.execute_LD_r_r, r1_index=4, r2_index=4),  # LD E, E
            0x5C: partial(self.execute_LD_r_r, r1_index=4, r2_index=6),  # LD E, H
            0x5D: partial(self.execute_LD_r_r, r1_index=4, r2_index=7),  # LD E, L
            0x5E: partial(self.execute_LD_r_HL, r_index=4),  # LD E, (HL)
            0x5F: partial(self.execute_LD_r_r, r1_index=4, r2_index=0),  # LD E, A
            0x60: partial(self.execute_LD_r_r, r1_index=6, r2_index=1),  # LD H, B
            0x61: partial(self.execute_LD_r_r, r1_index=6, r2_index=2),  # LD H, C
            0x62: partial(self.execute_LD_r_r, r1_index=6, r2_index=3),  # LD H, D
            0x63: partial(self.execute_LD_r_r, r1_index=6, r2_index=4),  # LD H, E
            0x64: partial(self.execute_LD_r_r, r1_index=6, r2_index=6),  # LD H, H
            0x65: partial(self.execute_LD_r_r, r1_index=6, r2_index=7),  # LD H, L
            0x66: partial(self.execute_LD_r_HL, r_index=6),  # LD H, (HL)
            0x67: partial(self.execute_LD_r_r, r1_index=6, r2_index=0),  # LD H, A
            0x68: partial(self.execute_LD_r_r, r1_index=7, r2_index=1),  # LD L, B
            0x69: partial(self.execute_LD_r_r, r1_index=7, r2_index=2),  # LD L, C
            0x6A: partial(self.execute_LD_r_r, r1_index=7, r2_index=3),  # LD L, D
            0x6B: partial(self.execute_LD_r_r, r1_index=7, r2_index=4),  # LD L, E
            0x6C: partial(self.execute_LD_r_r, r1_index=7, r2_index=6),  # LD L, H
            0x6D: partial(self.execute_LD_r_r, r1_index=7, r2_index=7),  # LD L, L
            0x6E: partial(self.execute_LD_r_HL, r_index=7),  # LD L, (HL)
            0x6F: partial(self.execute_LD_r_r, r1_index=7, r2_index=0),  # LD L, A
            0x70: partial(self.execute_LD_HL_r, r_index=1),  # LD (HL), B
            0x71: partial(self.execute_LD_HL_r, r_index=2),  # LD (HL), C
            0x72: partial(self.execute_LD_HL_r, r_index=3),  # LD (HL), D
            0x73: partial(self.execute_LD_HL_r, r_index=4),  # LD (HL), E
            0x74: partial(self.execute_LD_HL_r, r_index=6),  # LD (HL), H
            0x75: partial(self.execute_LD_HL_r, r_index=7),  # LD (HL), L
            0x76: self.execute_HALT,  # HALT
            0x77: partial(self.execute_LD_HL_r, r_index=0),  # LD (HL), A
            0x78: partial(self.execute_LD_r_r, r1_index=0, r2_index=1),  # LD A, B
            0x79: partial(self.execute_LD_r_r, r1_index=0, r2_index=2),  # LD A, C
            0x7A: partial(self.execute_LD_r_r, r1_index=0, r2_index=3),  # LD A, D
            0x7B: partial(self.execute_LD_r_r, r1_index=0, r2_index=4),  # LD A, E
            0x7C: partial(self.execute_LD_r_r, r1_index=0, r2_index=6),  # LD A, H
            0x7D: partial(self.execute_LD_r_r, r1_index=0, r2_index=7),  # LD A, L
            0x7E: partial(self.execute_LD_r_HL, r_index=0),  # LD A, (HL)
            0x7F: partial(self.execute_LD_r_r, r1_index=0, r2_index=0),  # LD A, A
            0x80: partial(self.execute_ALU_A, operation="add", r_index=1),  # ADD A, B
            0x81: partial(self.execute_ALU_A, operation="add", r_index=2),  # ADD A, C
            0x82: partial(self.execute_ALU_A, operation="add", r_index=3),  # ADD A, D
            0x83: partial(self.execute_ALU_A, operation="add", r_index=4),  # ADD A, E
            0x84: partial(self.execute_ALU_A, operation="add", r_index=6),  # ADD A, H
            0x85: partial(self.execute_ALU_A, operation="add", r_index=7),  # ADD A, L
            0x86: partial(self.execute_ALU_A, operation="add", r_index=None, indirect=True),  # ADD A, (HL)
            0x87: partial(self.execute_ALU_A, operation="add", r_index=0),  # ADD A, A
            0x88: partial(self.execute_ALU_A, operation="adc", r_index=1),  # ADC A, B
            0x89: partial(self.execute_ALU_A, operation="adc", r_index=2),  # ADC A, C
            0x8A: partial(self.execute_ALU_A, operation="adc", r_index=3),  # ADC A, D
            0x8B: partial(self.execute_ALU_A, operation="adc", r_index=4),  # ADC A, E
            0x8C: partial(self.execute_ALU_A, operation="adc", r_index=6),  # ADC A, H
            0x8D: partial(self.execute_ALU_A, operation="adc", r_index=7),  # ADC A, L
            0x8E: partial(self.execute_ALU_A, operation="adc", r_index=None, indirect=True),  # ADC A, (HL)
            0x8F: partial(self.execute_ALU_A, operation="adc", r_index=0),  # ADC A, A
            0x90: partial(self.execute_ALU_A, operation="sub", r_index=1),  # SUB B
            0x91: partial(self.execute_ALU_A, operation="sub", r_index=2),  # SUB C
            0x92: partial(self.execute_ALU_A, operation="sub", r_index=3),  # SUB D
            0x93: partial(self.execute_ALU_A, operation="sub", r_index=4),  # SUB E
            0x94: partial(self.execute_ALU_A, operation="sub", r_index=6),  # SUB H
            0x95: partial(self.execute_ALU_A, operation="sub", r_index=7),  # SUB L
            0x96: partial(self.execute_ALU_A, operation="sub", r_index=None, indirect=True),  # SUB (HL)
            0x97: partial(self.execute_ALU_A, operation="sub", r_index=0),  # SUB A
            0x98: partial(self.execute_ALU_A, operation="sbc", r_index=1),  # SBC A, B
            0x99: partial(self.execute_ALU_A, operation="sbc", r_index=2),  # SBC A, C
            0x9A: partial(self.execute_ALU_A, operation="sbc", r_index=3),  # SBC A, D
            0x9B: partial(self.execute_ALU_A, operation="sbc", r_index=4),  # SBC A, E
            0x9C: partial(self.execute_ALU_A, operation="sbc", r_index=6),  # SBC A, H
            0x9D: partial(self.execute_ALU_A, operation="sbc", r_index=7),  # SBC A, L
            0x9E: partial(self.execute_ALU_A, operation="sbc", r_index=None, indirect=True),  # SBC A, (HL)
            0x9F: partial(self.execute_ALU_A, operation="sbc", r_index=0),  # SBC A, A
            0xA0: partial(self.execute_ALU_A, operation="and", r_index=1),  # AND B
            0xA1: partial(self.execute_ALU_A, operation="and", r_index=2),  # AND C
            0xA2: partial(self.execute_ALU_A, operation="and", r_index=3),  # AND D
            0xA3: partial(self.execute_ALU_A, operation="and", r_index=4),  # AND E
            0xA4: partial(self.execute_ALU_A, operation="and", r_index=6),  # AND H
            0xA5: partial(self.execute_ALU_A, operation="and", r_index=7),  # AND L
            0xA6: partial(self.execute_ALU_A, operation="and", r_index=None, indirect=True),  # AND (HL)
            0xA7: partial(self.execute_ALU_A, operation="and", r_index=0),  # AND A
            0xA8: partial(self.execute_ALU_A, operation="xor", r_index=1),  # XOR B
            0xA9: partial(self.execute_ALU_A, operation="xor", r_index=2),  # XOR C
            0xAA: partial(self.execute_ALU_A, operation="xor", r_index=3),  # XOR D
            0xAB: partial(self.execute_ALU_A, operation="xor", r_index=4),  # XOR E
            0xAC: partial(self.execute_ALU_A, operation="xor", r_index=6),  # XOR H
            0xAD: partial(self.execute_ALU_A, operation="xor", r_index=7),  # XOR L
            0xAE: partial(self.execute_ALU_A, operation="xor", r_index=None, indirect=True),  # XOR (HL)
            0xAF: partial(self.execute_ALU_A, operation="xor", r_index=0),  # XOR A
            0xB0: partial(self.execute_ALU_A, operation="or", r_index=1),  # OR B
            0xB1: partial(self.execute_ALU_A, operation="or", r_index=2),  # OR C
            0xB2: partial(self.execute_ALU_A, operation="or", r_index=3),  # OR D
            0xB3: partial(self.execute_ALU_A, operation="or", r_index=4),  # OR E
            0xB4: partial(self.execute_ALU_A, operation="or", r_index=6),  # OR H
            0xB5: partial(self.execute_ALU_A, operation="or", r_index=7),  # OR L
            0xB6: partial(self.execute_ALU_A, operation="or", r_index=None, indirect=True),  # OR (HL)
            0xB7: partial(self.execute_ALU_A, operation="or", r_index=0),  # OR A
            0xB8: partial(self.execute_ALU_A, operation="cp", r_index=1),  # CP B
            0xB9: partial(self.execute_ALU_A, operation="cp", r_index=2),  # CP C
            0xBA: partial(self.execute_ALU_A, operation="cp", r_index=3),  # CP D
            0xBB: partial(self.execute_ALU_A, operation="cp", r_index=4),  # CP E
            0xBC: partial(self.execute_ALU_A, operation="cp", r_index=6),  # CP H
            0xBD: partial(self.execute_ALU_A, operation="cp", r_index=7),  # CP L
            0xBE: partial(self.execute_ALU_A, operation="cp", r_index=None, indirect=True),  # CP (HL)
            0xBF: partial(self.execute_ALU_A, operation="cp", r_index=0),  # CP A

            # Stack operations
            0xC0: partial(self.execute_RET_cc, condition='NZ'),  # RET NZ
            0xC1: partial(self.execute_POP_rr, r1_index=1, r2_index=2),  # POP BC
            0xC2: partial(self.execute_JP_cc, condition='NZ'),  # JP NZ, nn
            0xC3: self.execute_JP,  # JP nn
            0xC4: partial(self.execute_CALL_cc, condition='NZ'),  # CALL NZ, nn
            0xC5: partial(self.execute_PUSH_rr, r1_index=1, r2_index=2),  # PUSH BC
            0xC6: self.execute_ADD_A_n,  # ADD A, n
            0xC7: partial(self.execute_RST, address=0x00),  # RST 00H
            0xC8: partial(self.execute_RET_cc, condition='Z'),  # RET Z
            0xC9: self.execute_RET,  # RET
            0xCA: partial(self.execute_JP_cc, condition='Z'),  # JP Z, nn
            0xCB: self.execute_CB_prefix,  # Handle CB prefix
            0xCC: partial(self.execute_CALL_cc, condition='Z'),  # CALL Z, nn
            0xCD: self.execute_CALL,  # CALL nn
            0xCE: self.execute_ADC_A_n,  # ADC A, n
            0xCF: partial(self.execute_RST, address=0x08),  # RST 08H
            0xD0: partial(self.execute_RET_cc, condition='NC'),  # RET NC
            0xD1: partial(self.execute_POP_rr, r1_index=3, r2_index=4),  # POP DE
            0xD2: partial(self.execute_JP_cc, condition='NC'),  # JP NC, nn
            0xD4: partial(self.execute_CALL_cc, condition='NC'),  # CALL NC, nn
            0xD5: partial(self.execute_PUSH_rr, r1_index=3, r2_index=4),  # PUSH DE
            0xD6: self.execute_SUB_n,  # SUB n
            0xD7: partial(self.execute_RST, address=0x10),  # RST 10H
            0xD8: partial(self.execute_RET_cc, condition='C'),  # RET C
            0xD9: self.execute_RETI,  # RETI
            0xDA: partial(self.execute_JP_cc, condition='C'),  # JP C, nn
            0xDC: partial(self.execute_CALL_cc, condition='C'),  # CALL C, nn
            0xDE: self.execute_SBC_A_n,  # SBC A, n
            0xDF: partial(self.execute_RST, address=0x18),  # RST 18H
            0xE0: self.execute_LDH_n_A,  # LDH (n), A
            0xE1: partial(self.execute_POP_rr, r1_index=6, r2_index=7),  # POP HL
            0xE2: self.execute_LD_C_A,  # LD (C), A
            0xE5: partial(self.execute_PUSH_rr, r1_index=6, r2_index=7),  # PUSH HL
            0xE6: self.execute_AND_n,  # AND n
            0xE7: partial(self.execute_RST, address=0x20),  # RST 20H
            0xE8: self.execute_ADD_SP_n,  # ADD SP, n
            0xE9: self.execute_JP_HL,  # JP (HL)
            0xEA: self.execute_LD_nn_A,  # LD (nn), A
            0xEE: self.execute_XOR_n,  # XOR n
            0xEF: partial(self.execute_RST, address=0x28),  # RST 28H
            0xF0: self.execute_LDH_A_n,  # LDH A, (n)
            0xF1: partial(self.execute_POP_rr, r1_index=0, r2_index=5),  # POP AF
            0xF2: self.execute_LD_A_C,  # LD A, (C)
            0xF3: self.execute_DI,  # DI
            0xF5: partial(self.execute_PUSH_rr, r1_index=0, r2_index=5),  # PUSH AF
            0xF6: self.execute_OR_n,  # OR n
            0xF7: partial(self.execute_RST, address=0x30),  # RST 30H
            0xF8: self.execute_LD_HL_SP_n,  # LD HL, SP+n
            0xF9: self.execute_LD_SP_HL,  # LD SP, HL
            0xFA: self.execute_LD_A_nn,  # LD A, (nn)
            0xFB: self.execute_EI,  # EI
            0xFE: self.execute_CP_n,  # CP n
            0xFF: partial(self.execute_RST, address=0x38),  # RST 38H
        }
    

    def execute_NOP(self):
        pass

    def execute_HALT(self):
        self.emulator.halted = True

    def execute_STOP(self):
        self.emulator.stopped = True

    def execute_DI(self):
        self.emulator.interrupts_enabled = False

    def execute_EI(self):
        self.emulator.interrupts_enabled = True

    def execute_LD_r_n(self, r_index):
        self.emulator.registers[r_index] = self.emulator.fetch_instruction()

    def execute_LD_A_r(self, r_index, indirect=False):
        if indirect:
            address = (self.emulator.registers[r_index] << 8) | self.emulator.registers[r_index + 1]
            self.emulator.registers[0] = self.emulator.read_memory(address)
        else:
            self.emulator.registers[0] = self.emulator.registers[r_index]

    def execute_ALU_A(self, operation, r_index=None, indirect=False):
        if indirect:
            address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
            value = self.emulator.read_memory(address)
        else:
            value = self.emulator.registers[r_index]
        if operation == "add":
            result = self.emulator.registers[0] + value
        elif operation == "adc":
            result = self.emulator.registers[0] + value + self.emulator.flags['C']
        elif operation == "sub":
            result = self.emulator.registers[0] - value
        elif operation == "sbc":
            result = self.emulator.registers[0] - value - self.emulator.flags['C']
        elif operation == "and":
            result = self.emulator.registers[0] & value
        elif operation == "xor":
            result = self.emulator.registers[0] ^ value
        elif operation == "or":
            result = self.emulator.registers[0] | value
        elif operation == "cp":
            result = self.emulator.registers[0] - value
        self.update_flags(result)
        
    def update_flags(self, result):
        self.emulator.flags['Z'] = result == 0
        self.emulator.flags['N'] = False
        self.emulator.flags['H'] = False
        self.emulator.flags['C'] = result > 0xFF

    def execute_LD_r_HL(self, r_index):
        address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.registers[r_index] = self.emulator.read_memory(address)

    def execute_LD_HL_r(self, r_index):
        address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.write_memory(address, self.emulator.registers[r_index])

    def execute_JP(self, condition=None):
        address = self.fetch_16bit_operand()
        if condition is None or self.emulator.check_condition(condition):
            self.emulator.registers[9] = address

    def execute_CALL(self, condition=None):
        address = self.fetch_16bit_operand()
        if condition is None or self.emulator.check_condition(condition):
            self.push_pc_to_stack()
            self.emulator.registers[9] = address

    def execute_RET(self):
        self.emulator.registers[9] = self.emulator.pop_from_stack()

    def execute_RET_cc(self, condition):
        if self.emulator.check_condition(condition):
            self.execute_RET()

    def execute_RST(self, address):
        self.push_pc_to_stack()
        self.emulator.registers[9] = address

    def execute_CB_prefix(self):
        next_byte = self.emulator.fetch_instruction()
        if next_byte in self.emulator.opcode_map:
            self.emulator.opcode_map[next_byte]()

    def execute_LD_nn_SP(self):
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        address = (high << 8) | low
        self.emulator.write_memory(address, self.emulator.registers[8] & 0xFF)  # SP Low
        self.emulator.write_memory(address + 1, (self.emulator.registers[8] >> 8) & 0xFF)  # SP High

    def execute_LD_DE_A(self):
        de_address = (self.emulator.registers[3] << 8) | self.emulator.registers[4]
        self.emulator.write_memory(de_address, self.emulator.registers[0])  # Register A

    def execute_LDI_HL_A(self):
        hl_address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.write_memory(hl_address, self.emulator.registers[0])  # Register A
        hl_address += 1  # Increment HL
        self.emulator.registers[6] = (hl_address >> 8) & 0xFF
        self.emulator.registers[7] = hl_address & 0xFF

    def execute_LDI_A_HL(self):
        hl_address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.registers[0] = self.emulator.read_memory(hl_address)  # Load into A
        hl_address += 1  # Increment HL
        self.emulator.registers[6] = (hl_address >> 8) & 0xFF
        self.emulator.registers[7] = hl_address & 0xFF

    def execute_LDD_HL_A(self):
        hl_address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.write_memory(hl_address, self.emulator.registers[0])  # Register A
        hl_address -= 1  # Decrement HL
        self.emulator.registers[6] = (hl_address >> 8) & 0xFF
        self.emulator.registers[7] = hl_address & 0xFF

    def execute_LDD_A_HL(self):
        hl_address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.registers[0] = self.emulator.read_memory(hl_address)  # Load into A
        hl_address -= 1  # Decrement HL
        self.emulator.registers[6] = (hl_address >> 8) & 0xFF
        self.emulator.registers[7] = hl_address & 0xFF

    def execute_LD_SP_nn(self):
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        self.emulator.registers[8] = (high << 8) | low  # SP is index 8

    def execute_INC_SP(self):
        self.emulator.registers[8] += 1

    def execute_DEC_SP(self):
        self.emulator.registers[8] -= 1

    def execute_LD_HL_n(self):
        address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.write_memory(address, self.emulator.fetch_instruction())

    def execute_ALU_n(self, operation):
        value = self.emulator.fetch_instruction()
        if operation == "add":
            result = self.emulator.registers[0] + value
        elif operation == "adc":
            result = self.emulator.registers[0] + value + self.emulator.flags['C']
        elif operation == "sub":
            result = self.emulator.registers[0] - value
        elif operation == "sbc":
            result = self.emulator.registers[0] - value - self.emulator.flags['C']
        elif operation == "and":
            result = self.emulator.registers[0] & value
        elif operation == "xor":
            result = self.emulator.registers[0] ^ value
        elif operation == "or":
            result = self.emulator.registers[0] | value
        elif operation == "cp":
            result = self.emulator.registers[0] - value
        self.update_flags(result)

    def execute_LD_A_nn(self):
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        address = (high << 8) | low
        self.emulator.registers[0] = self.emulator.read_memory(address)  # Load A from (nn)

    def execute_LD_nn_A(self):
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        address = (high << 8) | low
        self.emulator.write_memory(address, self.emulator.registers[0])  # Store A to (nn)

    def execute_LD_A_C(self):
        address = 0xFF00 + self.emulator.registers[2]  # C is register index 2
        self.emulator.registers[0] = self.emulator.read_memory(address)

    def execute_LD_C_A(self):
        address = 0xFF00 + self.emulator.registers[2]  # C is register index 2
        self.emulator.write_memory(address, self.emulator.registers[0])

    def execute_LDH_n_A(self):
        address = 0xFF00 + self.emulator.fetch_instruction()
        self.emulator.write_memory(address, self.emulator.registers[0])

    def execute_LDH_A_n(self):
        address = 0xFF00 + self.emulator.fetch_instruction()
        self.emulator.registers[0] = self.emulator.read_memory(address)

    def execute_INC_r(self, r_index):
        self.emulator.registers[r_index] += 1
        self.update_flags_for_inc(self.emulator.registers[r_index])

    def execute_DEC_r(self, r_index):
        self.emulator.registers[r_index] -= 1
        self.update_flags_for_dec(self.emulator.registers[r_index])

    def execute_INC_rr(self, r1_index, r2_index):
        value = (self.emulator.registers[r1_index] << 8) + self.emulator.registers[r2_index] + 1
        self.emulator.registers[r1_index] = (value >> 8) & 0xFF
        self.emulator.registers[r2_index] = value & 0xFF

    def execute_DEC_rr(self, r1_index, r2_index):
        value = (self.emulator.registers[r1_index] << 8) + self.emulator.registers[r2_index] - 1
        self.emulator.registers[r1_index] = (value >> 8) & 0xFF
        self.emulator.registers[r2_index] = value & 0xFF

    def execute_RLCA(self):
        a = self.emulator.registers[0]
        carry = (a >> 7) & 1
        self.emulator.registers[0] = ((a << 1) | carry) & 0xFF
        self.emulator.flags['C'] = carry

    def execute_RRCA(self):
        a = self.emulator.registers[0]
        carry = a & 1
        self.emulator.registers[0] = ((carry << 7) | (a >> 1)) & 0xFF
        self.emulator.flags['C'] = carry

    def execute_RLA(self):
        a = self.emulator.registers[0]
        old_carry = self.emulator.flags['C']
        new_carry = (a >> 7) & 1
        self.emulator.registers[0] = ((a << 1) | old_carry) & 0xFF
        self.emulator.flags['C'] = new_carry

    def execute_RRA(self):
        a = self.emulator.registers[0]
        old_carry = self.emulator.flags['C']
        new_carry = a & 1
        self.emulator.registers[0] = ((old_carry << 7) | (a >> 1)) & 0xFF
        self.emulator.flags['C'] = new_carry

    def execute_CPL(self):
        self.emulator.registers[0] = ~self.emulator.registers[0] & 0xFF
        self.emulator.flags['N'] = 1
        self.emulator.flags['H'] = 1

    def execute_SCF(self):
        self.emulator.flags['C'] = 1
        self.emulator.flags['N'] = 0
        self.emulator.flags['H'] = 0

    def execute_CCF(self):
        self.emulator.flags['C'] = not self.emulator.flags['C']
        self.emulator.flags['N'] = 0
        self.emulator.flags['H'] = 0

    def execute_POP_rr(self, r1_index, r2_index):
        sp = self.emulator.registers[8]
        self.emulator.registers[r2_index] = self.emulator.read_memory(sp)
        self.emulator.registers[r1_index] = self.emulator.read_memory(sp + 1)
        self.emulator.registers[8] += 2

    def execute_PUSH_rr(self, r1_index, r2_index):
        sp = self.emulator.registers[8]
        self.emulator.write_memory(sp - 1, self.emulator.registers[r1_index])
        self.emulator.write_memory(sp - 2, self.emulator.registers[r2_index])
        self.emulator.registers[8] -= 2

    def execute_ADD_SP_n(self):
        n = self.emulator.fetch_instruction()
        if n > 127:
            n -= 256
        self.emulator.registers[8] = (self.emulator.registers[8] + n) & 0xFFFF
        self.update_flags_for_add(self.emulator.registers[8], self.emulator.registers[8] + n, None)

    def execute_JP_HL(self):
        hl = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        self.emulator.registers[9] = hl

    def execute_LD_HL_SP_n(self):
        n = self.emulator.fetch_instruction()
        if n > 127:
            n -= 256
        self.emulator.registers[6] = (self.emulator.registers[8] + n) >> 8
        self.emulator.registers[7] = (self.emulator.registers[8] + n) & 0xFF
        self.update_flags_for_add(self.emulator.registers[6], self.emulator.registers[6] + n, None)

    def execute_RETI(self):
        self.execute_RET()
        self.execute_EI()

    def execute_CP_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] - value
        self.update_flags_for_sub(self.emulator.registers[0], result, None)

    def update_flags_for_add(self, actual, result, r_index):
        self.emulator.flags['Z'] = 1 if actual == 0 else 0
        self.emulator.flags['N'] = 0
        self.emulator.flags['H'] = 1 if (self.emulator.registers[0] & 0xF) + (self.emulator.registers[r_index] & 0xF) > 0xF else 0
        self.emulator.flags['C'] = 1 if result > 255 else 0
            
    def update_flags_for_sub(self, actual, result, r_index):
        self.emulator.flags['Z'] = 1 if result == 0 else 0
        self.emulator.flags['N'] = 1
        if r_index is not None:
            self.emulator.flags['H'] = 1 if (self.emulator.registers[0] & 0xF) < (self.emulator.registers[r_index] & 0xF) else 0
        else:
            self.emulator.flags['H'] = 1 if (actual & 0xF) < (result & 0xF) else 0
        self.emulator.flags['C'] = 1 if result < 0 else 0
    
    def execute_LD_rr_nn(self, r1_index, r2_index):
        """ Load immediate 16-bit value nn into register pair rr. """
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        self.emulator.registers[r1_index] = high
        self.emulator.registers[r2_index] = low

    def execute_LD_indirect_A(self, address_reg):
        address = (self.emulator.registers[address_reg] << 8) | self.emulator.registers[address_reg + 1]
        self.emulator.write_memory(address, self.emulator.registers[0])  # Store A at the address in the register pair

    def execute_LD_A_indirect(self, address_reg):
        address = (self.emulator.registers[address_reg] << 8) | self.emulator.registers[address_reg + 1]
        self.emulator.registers[0] = self.emulator.read_memory(address)  # Load A from the address in the register pair

    def execute_JR(self):
        offset = self.fetch_signed_operand()
        self.emulator.registers[9] += offset

    def execute_JR_cc(self, condition):
        offset = self.fetch_signed_operand()
        if self.check_condition(condition):
            self.emulator.registers[9] += offset

    def execute_LD_r_r(self, r1_index, r2_index):
        self.emulator.registers[r1_index] = self.emulator.registers[r2_index]

    def execute_ADD_HL_rr(self, r1_index, r2_index):
        hl = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        rr = (self.emulator.registers[r1_index] << 8) | self.emulator.registers[r2_index]
        result = hl + rr
        self.emulator.registers[6] = (result >> 8) & 0xFF
        self.emulator.registers[7] = result & 0xFF
        self.update_flags_for_add(result, result, None)

    def execute_CALL_cc(self, condition):
        address = self.fetch_16bit_operand()
        if self.check_condition(condition):
            self.push_pc_to_stack()
            self.emulator.registers[9] = address

    def update_flags_for_logic(self, result):
        self.emulator.flags['Z'] = 1 if result == 0 else 0
        self.emulator.flags['N'] = 0
        self.emulator.flags['H'] = 1
        self.emulator.flags['C'] = 0

    def check_condition(self, condition):
        if condition == 'Z':
            return self.emulator.flags['Z'] == 1
        elif condition == 'NZ':
            return self.emulator.flags['Z'] == 0
        elif condition == 'C':
            return self.emulator.flags['C'] == 1
        elif condition == 'NC':
            return self.emulator.flags['C'] == 0
        return False

    def fetch_16bit_operand(self):
        low = self.emulator.fetch_instruction()
        high = self.emulator.fetch_instruction()
        return (high << 8) | low

    def fetch_signed_operand(self):
        value = self.emulator.fetch_instruction()
        return value - 256 if value > 127 else value

    def push_pc_to_stack(self):
        sp = self.emulator.registers[8]
        pc = self.emulator.registers[9]
        self.emulator.write_memory(sp - 1, (pc >> 8) & 0xFF)
        self.emulator.write_memory(sp - 2, pc & 0xFF)
        self.emulator.registers[8] -= 2

    def pop_from_stack(self):
        sp = self.emulator.registers[8]
        low = self.emulator.read_memory(sp)
        high = self.emulator.read_memory(sp + 1)
        self.emulator.registers[8] += 2
        return (high << 8) | low
    
    def execute_ADD_A_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] + value
        self.update_flags_for_add(result, result, None)
        self.emulator.registers[0] = result & 0xFF

    def execute_ADC_A_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] + value + self.emulator.flags['C']
        self.update_flags_for_add(result, result, None)
        self.emulator.registers[0] = result & 0xFF

    def execute_SUB_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] - value
        self.update_flags_for_sub(result, result, None)
        self.emulator.registers[0] = result & 0xFF

    def execute_SBC_A_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] - value - self.emulator.flags['C']
        self.update_flags_for_sub(result, result, None)
        self.emulator.registers[0] = result & 0xFF

    def execute_AND_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] & value
        self.update_flags_for_logic(result)
        self.emulator.registers[0] = result

    def execute_XOR_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] ^ value
        self.update_flags_for_logic(result)
        self.emulator.registers[0] = result

    def execute_OR_n(self):
        value = self.emulator.fetch_instruction()
        result = self.emulator.registers[0] | value
        self.update_flags_for_logic(result)
        self.emulator.registers[0] = result

    def execute_INC_HL(self):
        address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        value = self.emulator.read_memory(address) + 1
        self.emulator.write_memory(address, value & 0xFF)
        self.update_flags_for_inc(value)

    def execute_DEC_HL(self):
        address = (self.emulator.registers[6] << 8) | self.emulator.registers[7]
        value = self.emulator.read_memory(address) - 1
        self.emulator.write_memory(address, value & 0xFF)
        self.update_flags_for_dec(value)

    def execute_LD_A_n(self):
        self.emulator.registers[0] = self.emulator.fetch_instruction()

    def update_flags_for_inc(self, value):
        self.emulator.flags['Z'] = 1 if (value & 0xFF) == 0 else 0
        self.emulator.flags['N'] = 0
        self.emulator.flags['H'] = 1 if (value & 0xF) == 0 else 0

    def update_flags_for_dec(self, value):
        self.emulator.flags['Z'] = 1 if (value & 0xFF) == 0 else 0
        self.emulator.flags['N'] = 1
        self.emulator.flags['H'] = 1 if (value & 0xF) == 0xF else 0

    def execute_JP_cc(self, condition):
        address = self.fetch_16bit_operand()
        if self.check_condition(condition):
            self.emulator.registers[9] = address
    
    def execute_LD_SP_HL(self):
        self.emulator.registers[8] = (self.emulator.registers[6] << 8) | self.emulator.registers[7]