##########################################################################
# This file is part of d00ks.
# 
# d00ks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# d00ks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with d00ks.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################


print "COMPILING PARSER..."
from parser import *

prog = """
AREA Primes, CODE, READONLY

start
	MOV R5, #1
	MOV R6, #0
loop
	CMP R5, #1000
	BGE stop
	MOV R0, R5
	MOV R1, #3
	BL divmod
	CMP R0, #0
	BEQ win
	MOV R0, R5
	MOV R1, #5
	BL divmod
	CMP R0, #0
	BEQ win
	B next
win
	ADD R6, R6, R5
next
	ADD R5, R5, #1
	B loop

; stores quotient in R1, remainder in R0
divmod
	MOV R3, #0
divmod_while
	CMP R1, #0
	BEQ divmod_err
	CMP R0, R1
	BLT divmod_done
	ADD R3, R3, #1
	SUB R0, R0, R1
	B divmod_while
divmod_err
	MOV R3, #0xFFFFFFFF
divmod_done
	MOV R1, R3
	MOV PC, LR


stop B stop

"""

print "INPUT:"
i = 1
for line in prog.split("\n"):
	print "%i %s"%(i, line)
	i = i + 1
print ""
print "COMPILING."

import pprint
pp = pprint.PrettyPrinter()

output = parser.parse(prog)
pp.pprint(output)

program = simulator.program()
program.compile(output)

program.debug()
