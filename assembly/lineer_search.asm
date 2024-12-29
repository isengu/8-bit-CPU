; Lineer Search Algorithm

LDAI 0x00 ; initial value to begin for search
LDBI 0x0A ; the value to search for

STB 0xfd ; memory address fd -> the value to search for
STA 0xff ; memory address ff -> current value

COMPARE:
	SUB ; subtract B reg from A reg
	LDA 0xff ; load A reg with current value
	JZ END ; if zero jump end
	JMP INCREMENT ; if not zero jump increment

INCREMENT:
	LDBI 0x01
	ADD
	LDB 0xfd
	STA 0xff
	JMP COMPARE

END:
	OUT
	HLT