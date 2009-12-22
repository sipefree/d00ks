def EQ(r):
	"""Passes if zero flag is set."""
	if r[r.CPSR] & r.Z:
		return True
	else:
		return False

def NE(r):
	"""Passes is zero flag is not set."""
	return not EQ(r)

def CS(r):
	"""Passes if carry set / Unsigned higher or same"""
	if r[r.CPSR] & r.C:
		return True
	else:
		return False

def HS(r):
	return CS(r)


def CC(r):
	"""Passes if carry clear / Unsigned lower"""
	return not CS(r)


def LO(r):
	return CC(r)

	
def MI(r):
	"""Passes if negative flag is set / Less than"""
	if r[r.CPSR] & r.N:
		return True
	else:
		return False

def PL(r):
	"""Passes if positive or zero"""
	return not MI(r)

def VS(r):
	"""Passes if overflow set"""
	if r[r.CPSR] & r.V:
		return True
	else:
		return False

def VC(r):
	"""Passes if overflow not set"""
	return VS(r)

def HI(r):
	"""Unsigned higher / C and not Z"""
	return CS(r) and not EQ(r)

def LS(r):
	"""Unsigned lower or same"""
	return (not CS(r)) or EQ(r)

def GE(r):
	"""Signed greater than or equal"""
	return (MI(r) and VS(r)) or ((not MI(r)) and (not VS(r)))

def LT(r):
	"""Signed less than"""
	return (MI(r) and (not VS(r))) or ((not MI(r)) and VS(r))

def GT(r):
	"""Signed greater than"""
	return (not EQ(r)) and (GE(r))

def LE(r):
	"""Signed less than or equal"""
	return EQ(r) or LT(r)

def AL(R):
	"""Always"""
	return True

AL.__name__ = ""
