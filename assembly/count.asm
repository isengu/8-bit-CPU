LDAI 0x0
LDBI 0x1

COUNT:
	ADD
	OUT
	JC END
	JMP COUNT

END:
	LDAI 0xff
	OUT
	HLT