import pandas as pd
import itertools

filename = "../../instructions_control_details.xlsx"
sheet_names = ['Instruction Set', 'States and Corresponding Contro', 'Instruction States', 'States Detailed']

sheet_data = {}
for sheet_name in sheet_names:
    sheet_data[sheet_name] = pd.read_excel(filename, na_filter=False, sheet_name=sheet_name, converters = {"Control Word Binary Form": str})

rom_data = {
    format(i, '010b'): '10000' for i in range(1024)
}

states_to_binary_word = {
	int(sheet_data[sheet_names[1]]["State Number"][i]): sheet_data[sheet_names[1]]["Control Word Binary Form"][i]
		for i in range(sheet_data[sheet_names[1]].shape[0])
}


def build_addresses_to_states():
	[row_count, column_count] = sheet_data[sheet_names[3]].shape

	opcodes = sheet_data[sheet_names[3]]["Op Code"]
	carry_flags = sheet_data[sheet_names[3]]["Carry Flag"]
	zero_flags = sheet_data[sheet_names[3]]["Zero Flag"]
	micro_steps = sheet_data[sheet_names[3]]["Micro Step"]
	states = sheet_data[sheet_names[3]]["State"]

	opcode_values = []
	carry_flag_values = []
	zero_flag_values = []
	micro_step_values = []

	for i in range(row_count):
		opcode_value = []
		carry_flag_value = []
		zero_flag_value = []
		micro_step_value = []

		# skip empty values
		if opcodes[i] == '':
			continue

		if opcodes[i] == "x":
			opcode_value = generate_all_binary_combinations(5)
		else:
			opcode_value.append(format(int(opcodes[i], 16), '05b'))

		if carry_flags[i] == "x":
			carry_flag_value = generate_all_binary_combinations(1)
		else:
			carry_flag_value.append(format(carry_flags[i], '01b'))

		if zero_flags[i] == "x":
			zero_flag_value = generate_all_binary_combinations(1)
		else:
			zero_flag_value.append(format(zero_flags[i], '01b'))

		micro_step_value.append(format(micro_steps[i], '03b'))

		opcode_values.append(opcode_value)
		carry_flag_values.append(carry_flag_value)
		zero_flag_values.append(zero_flag_value)
		micro_step_values.append(micro_step_value)

		state = states[i]
		addresses_of_state = ["".join(tup) for tup in itertools.product(opcode_value, carry_flag_value, zero_flag_value, micro_step_value)]

		if opcode_value[0] == "01101":
			print(addresses_of_state, state)

		for address in addresses_of_state:
			rom_data[address] = hex(int(states_to_binary_word[state], 2))[2:].zfill(5)

# generates all of the binary combinations for the given bit length
def generate_all_binary_combinations(bit_length):
	return [format(i, f'0{bit_length}b') for i in range(2**bit_length)]


if __name__ == "__main__":
	build_addresses_to_states()

	file_content = "v3.0 hex words plain\n"

	count = 0
	for e in rom_data.values():
		count+=1
		file_content += e + " "
		if count == 8:
			count = 0
			file_content += "\n"
	print(file_content.strip())

	with open('rom.hex', 'w') as file:
		file.write(file_content)