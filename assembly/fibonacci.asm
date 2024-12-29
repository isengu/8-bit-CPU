INIT:                   ; 0x00
	LDAI 0x00           ; Initializes the number 1 loading it in register A.
	STA 0xfe	        ; Stores register A in the number 1 memory address.
	OUT	        		; Output the number 1.

	LDAI 0x01          	; Initializes the number 2 loading it in register A.
	STA 0xff	        ; Stores register A in the number 2 memory address.

START:                  ; 0x0A
	OUT		        	; Output the number 2.
	LDA 0xfe	        ; Loads the number 1 in register A.
	LDB 0xff
	ADD	        		; Adds the number 2.
	STB 0xfe	        ; Stores number 2 in number 1.
	STA 0xff	        ; Stores the sum of number 1 and 2 in number 2.

	JC INIT        		; Jump on carry (restart).
	JMP START       	; Jumps to start.

; VARIABLES:
; 0xfe -> NUM1
; 0xff -> NUM2