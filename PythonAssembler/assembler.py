import os, sys

# Machine code of C-instruction
Ccode = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}
# Machine code of destination
destcode = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}
# Machine code of jumpcode
jumpcode = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}
# Standard symbols code
ssymb = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}

for i in range(0,16):
  label = "R" + str(i)
  ssymb[label] = i

# Store name of the ASM file
str = open('nhh.txt', 'r').read()
root = str  
variableCursor = 16    # Available memory location for variables, start from 16

# Removes whitespace and comments; return line without a closing \n
# lines[1:] generate a sub list of the line list, which begins from index 1
def strip(line):
  char = line[0]
  if char == "\n" or char == "/":
    return ""
  elif char == " ":
    return strip(line[1:])
  else:
    return char + strip(line[1:])

# Normalizes C-instructions by adding null destcode & jumpcode fields if they're unspecified
# line[:-1] generate a sub list of the line list without last character
def normalize(line):
  line = line[:-1]
  if not "=" in line:
    line = "null=" + line
  if not ";" in line:
    line = line + ";null"
  return line

# Allocates a memory location for new variables
def addVariable(label):
  global variableCursor
  ssymb[label] = variableCursor
  variableCursor = variableCursor + 1
  return ssymb[label]

# Translates a symbolic a-instruction into an int (if necessary) then translates that into a binary machine instruction
def aTranslate(line):
  if line[1].isalpha():
    label = line[1:-1]
    aValue = ssymb.get(label, -1)
    if aValue == -1:
      aValue = addVariable(label)
  else:
    aValue = int(line[1:])
  bValue = bin(aValue)[2:].zfill(16)
  return bValue
 
# Splits a C-instruction into its components & translates them
# get(temp[0], "destFAIL") return "destFAIL" if temp[0] not found
def cTranslate(line):
  line = normalize(line)
  temp = line.split("=")
  destCode = destcode.get(temp[0], "destFAIL")
  temp = temp[1].split(";")
  compCode = Ccode.get(temp[0], "compFAIL")
  jumpCode = jumpcode.get(temp[1], "jumpFAIL")
  return compCode, destCode, jumpCode

# Calls appropriate function to translate A or C-instruction
def translate(line):
  if line[0] == "@":
    return aTranslate(line)
  else:
    codes = cTranslate(line)
    return "111" + codes[0] + codes[1] + codes[2]

# Read ASM file for labels and enters them into the ssymb, strip out comments & empty lines
def firstPass():
  infile = open(root)
  outfile = open(root + ".tmp", "w")

  lineNumber = 0
  for line in infile:
    sline = strip(line)
    if sline != "":
      if sline[0] == "(":
        label = sline[1:-1]
        ssymb[label] = lineNumber
        sline = ""
      else:
        lineNumber = lineNumber + 1
        outfile.write(sline + "\n")

  infile.close()
  outfile.close()

# Take file stripped of labels and translate it into .hack
def assemble():
  infile = open(root + ".tmp")
  outfile = open(root + ".hack", "w")

  for line in infile:
    tline = translate(line)
    outfile.write(tline + "\n")

  infile.close()
  outfile.close()
  os.remove(root + ".tmp")
  os.remove("nhh.txt")


# Main program just call to these two functions
firstPass()
assemble()
