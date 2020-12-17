// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

(START)
	// Initialize product to 0
	@R2 //A = 2, RAM[2] is now selected, represented by M
	M = 0 //Set M equal to 0, RAM[2] now holds value 0

(LOOP) //Add R0 to R2 R1 times
	// If R1 <= 0, terminate
	@R1 //A = 1, RAM[1] is now selected, represented by M
	@END //A = The address of END segment
	M; JLE // Jump to A if M <= 0
	// Add R0 to R2
	@R0
	D = M
	@R2
	M = M + D
	// Decrease R1 (for the loop condition)
	@R1
	M = M - 1
	// Loop
	@LOOP
	0; JMP

(END)
	// Terminate
	@END
	0; JMP