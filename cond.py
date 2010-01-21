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


"""
This file contains condition functions which when given a set
of registers will return whether or not the condition passes,
given that conditions are based on the CPSR.
"""

import promise

@promise.sensible()
@promise.pure()
def EQ(r):
	"""Passes if zero flag is set."""
	return bool(r[r.CPSR] & r.Z)

@promise.sensible()
@promise.pure()
def NE(r):
	"""Passes is zero flag is not set."""
	return not bool(r[r.CPSR] & r.Z)

@promise.sensible()
@promise.pure()
def CS(r):
	"""Passes if carry set / Unsigned higher or same"""
	return bool(r[r.CPSR] & r.C)

@promise.sensible()
@promise.pure()
def HS(r):
	return bool(r[r.CPSR] & r.C)

@promise.sensible()
@promise.pure()
def CC(r):
	"""Passes if carry clear / Unsigned lower"""
	return not bool(r[r.CPSR] & r.C)

@promise.sensible()
@promise.pure()
def LO(r):
	return not bool(r[r.CPSR] & r.C)

@promise.sensible()
@promise.pure()
def MI(r):
	"""Passes if negative flag is set / Less than"""
	return bool(r[r.CPSR] & r.N)

@promise.sensible()
@promise.pure()
def PL(r):
	"""Passes if positive or zero"""
	return not bool(r[r.CPSR] & r.N)

@promise.sensible()
@promise.pure()
def VS(r):
	"""Passes if overflow set"""
	return bool(r[r.CPSR] & r.V)

@promise.sensible()
@promise.pure()
def VC(r):
	"""Passes if overflow not set"""
	return not bool(r[r.CPSR] & r.V)

@promise.sensible()
@promise.pure()
def HI(r):
	"""Unsigned higher / C and not Z"""
	return bool(r[r.CPSR] & r.C) and not bool(r[r.CPSR] & r.Z)

@promise.sensible()
@promise.pure()
def LS(r):
	"""Unsigned lower or same"""
	return (not bool(r[r.CPSR] & r.C)) or bool(r[r.CPSR] & r.Z)

@promise.sensible()
@promise.pure()
def GE(r):
	"""Signed greater than or equal"""
	return (bool(r[r.CPSR] & r.N) and bool(r[r.CPSR] & r.V)) or ((not bool(r[r.CPSR] & r.N)) and (not bool(r[r.CPSR] & r.V)))

@promise.sensible()
@promise.pure()
def LT(r):
	"""Signed less than"""
	return (bool(r[r.CPSR] & r.N) and (not bool(r[r.CPSR] & r.V))) or ((not bool(r[r.CPSR] & r.N)) and bool(r[r.CPSR] & r.V))

@promise.sensible()
@promise.pure()
def GT(r):
	"""Signed greater than"""
	return (not bool(r[r.CPSR] & r.Z)) and ((bool(r[r.CPSR] & r.N) and bool(r[r.CPSR] & r.V)) or ((not bool(r[r.CPSR] & r.N)) and (not bool(r[r.CPSR] & r.V))))

@promise.sensible()
@promise.pure()
def LE(r):
	"""Signed less than or equal"""
	return bool(r[r.CPSR] & r.Z) or (bool(r[r.CPSR] & r.N) and (not bool(r[r.CPSR] & r.V))) or ((not bool(r[r.CPSR] & r.N)) and bool(r[r.CPSR] & r.V))

@promise.sensible()
@promise.pure()
def AL(R):
	"""Always"""
	return True

AL.__name__ = ""
