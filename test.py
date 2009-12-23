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



from register import *
from cond import *
from instruction import *
from simulator import *

# instrs = [
# MOV(AL, False, 1, shifter(num(0xF))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0xF))),
# 
# MOV(AL, False, 1, shifter(num(0x0))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0x0))),
# 
# MOV(AL, False, 1, shifter(num(0xFFFFFFFF))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0x1))),
# 
# MOV(AL, False, 1, shifter(num(0xD0000000))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0x10000000))),
# 
# MOV(AL, False, 1, shifter(num(0xF0000000))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0x10000001))),
# 
# MOV(AL, False, 1, shifter(num(0xF0000000))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0xD0000000))),
# 
# MOV(AL, False, 1, shifter(num(0x40000000))),
# ADD(AL, True, 0, argument(True, 1), shifter(num(0x40000000))),
# ]

# instrs = [
# MOV(AL, False, 1, shifter(num(0x34FD1A82))),
# MOV(AL, False, 0, shifter(num(0x44810FA1))),
# MOV(AL, False, 3, shifter(num(0x4DC3A734))),
# MOV(AL, False, 2, shifter(num(0x277D1B90))),
# SUB(AL, True, 5, argument(True, 0), shifter(argument(True, 2))),
# SBC(AL, False, 4, argument(True, 1), shifter(argument(True, 3))),
# ]

instrs = [
# load a test value into R1
# MOV R1, #0xAC
MOV(AL, False, 1, shifter(num(0xAC))),

# AND R2, R1, #0x1
AND(AL, False, 2, R1, shifter(num(0x1))),
# MOV R0, R2, LSL #2
MOV(AL, False, 0, LSL(R2, num(2))),

# AND R2, R1, #0xE
AND(AL, False, 2, R1, shifter(num(0xE))),
# ORR R0, R0, R2, LSL #3
ORR(AL, False, 0, R0, LSL(R2, num(3))),

# AND R2, R1, #0xF0
AND(AL, False, 2, R1, shifter(num(0xF0))),
# ORR R0, R0, R2, LSL #4
ORR(AL, False, 0, R0, LSL(R2, num(4))),

# end B end
B(False, AL, target(True, "end")),
]

prog = program(instrs)

prog.registers.symbol_table["start"] = (0, instrs[0])
prog.registers.symbol_table["end"] = (7, instrs[7])
