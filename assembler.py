# "instruction" : ("opcode", "has_operand")
instructions = {
	"NOP": ("0x00", False),
	"HLT": ("0x01", False),
	"LDAI": ("0x02", True),
	"LDA": ("0x03", True),
	"STA": ("0x04", True),
	"LDBI": ("0x05", True),
	"LDB": ("0x06", True),
	"STB": ("0x07", True),
	"ADD": ("0x08", False),
	"SUB": ("0x09", False),
	"OUT": ("0x0A", False),
	"JMP": ("0x0B", True),
	"JZ": ("0x0C", True),
	"JC": ("0x0D", True)
}


label_to_address = {}
address_counter = 0
ram_data = {
    format(i, '08b'): '00' for i in range(256)
}

with open("../../count.asm", "r") as file:
	for l in file:
		line = l.split(";")[0].strip()

		if not line:
			continue;

		inst_parts = line.split()
		if len(inst_parts) > 2:
			print(f"[ERROR] invalid instruction definition. line: {line}")
			exit()

		instruction = inst_parts[0]
		operand = inst_parts[1] if len(inst_parts) > 1 else None

		if instruction[-1] == ":":
			label_to_address[instruction[:-1]] = address_counter
		else:
			[opcode_hex, inst_has_operand] = instructions[instruction]

			if not opcode_hex:
				print(f"[ERROR] invalid instruction. line: {line}")
				exit()

			if inst_has_operand and not operand:
				print(f"[ERROR] instruction must have operand. line: {line}")
				exit()
			
			if inst_has_operand:
				address_counter += 2
			else:
				address_counter += 1


address_counter=0
with open("../../count.asm", "r") as file:
	for l in file:
		line = l.split(";")[0].strip()

		if not line:
			continue;

		inst_parts = line.split()
		if len(inst_parts) > 2:
			print(f"[ERROR] invalid instruction definition. line: {line}")
			exit()

		instruction = inst_parts[0]
		operand = inst_parts[1] if len(inst_parts) > 1 else None

		if instruction[-1] != ":":
			[opcode_hex, inst_has_operand] = instructions[instruction]

			if inst_has_operand and label_to_address.get(operand):
				print(f"[INFO] {label_to_address[operand]}")
				operand = hex(label_to_address[operand])

			if inst_has_operand and operand[:2] != "0x":
				print(f"[ERROR] operand must be in hex format(0xff). line: {line}")
				exit()

			ram_data[format(address_counter, '08b')] = opcode_hex[2:].zfill(2)
			address_counter+=1
			if inst_has_operand:
				ram_data[format(address_counter, '08b')] = operand[2:].zfill(2)
				address_counter+=1

print(label_to_address)
file_content = "v3.0 hex words plain\n"

count = 0
for e in ram_data.values():
	count+=1
	file_content += e + " "
	if count == 8:
		count = 0
		file_content += "\n"
print(file_content.strip())

with open('ram.hex', 'w') as file:
	file.write(file_content)