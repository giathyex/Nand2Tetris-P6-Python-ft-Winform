// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(CHECK)
	// Set currentblock pointer to the first pixel block in screen pixel array
	// or reset pointer to first block (16384) if one loop was completed before
	@SCREEN
	D = A
	@currentblock
	M = D

	// Get input data from keyboard, store it to D
    @KBD
	D = M
    // Set fillvalue = -1, or 1111111111111111 in binary code
	@fillvalue
	M = -1
    // Jump to DRAW with fillvalue = -1 if D is not equal to 0 (blacken the screen)
	@DRAW
	D; JNE
	// Jump to DRAW with fillvalue = 0 if D is not equal to 0 (clear the screen)
	@fillvalue
	M = 0

(DRAW)
	// Load fillvalue to D
	@fillvalue
	D = M
    // Load currentblock data from pointer and fill it with fill value in D
	@currentblock
	A = M
	M = D

	// Check if all the blocks have been changed yet
	// If all blocks have been changed, current block will be the last block, which is 24575
	// So if current block is equal to 24575, the program go back to keyboard check
	@currentblock
	D = M
	@24575
	D = D - A
	@CHECK
	D; JGE
    
	// If all block have not been changed yet, continue
	// Point the currentblock pointer to next block
	@currentblock
	M = M + 1
	// Continue drawing next block
	@DRAW
	0; JMP
