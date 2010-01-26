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

import curses, os
from parser import *
from sys import argv

class gb: # global variables(ugly but works)

	screen = None
	output = []
	curline = None
	windows = {}
	dimensions = {'min': (80,30)}

class RegistersWindow:
	title = "registers"
	dimensions = {'min':(20,20), 'resizable': False, 'align':1}
	
	def __init__(self,position=(60,2),size=dimensions['min']):
		posx,posy = position
		sizex,sizey = size
		self.wo = curses.newwin(sizey,sizex,posy,posx)
		self.wo.addstr(0,1,self.title,curses.A_STANDOUT)
		for r in self.content:
			r[0] = '0x000000'
			r[1] = curses.A_NORMAL
	def setRegs(_regs ):
		"""setRegs(regs,cpsr,pc)
		a setter method for register window. accepts a list of registers,
		CPSR and PC """
		
		if gb.debugmode: #small, barely necessary performance hack.paranoia.
			for r in range(0,len(self.content)):
				if self.content[r][0] != _regs[r]:
					self.content[r][1] = True
				self.content[r][0] = _regs[r]
		else:
			for r in range(0,len(self.content)):
				self.content[r][0] = _regs[r]
				


	def draw():
		for r in range(0,16):
			self.wo.addstr(r+2, 2 , self.content[r][0],
					curses.A_BOLD if self.content[r][1] else curses.A_NORMAL)

		self.wo.overlay(gb.screen)

class MemoryWindow:
	title = "Memory View"
	dimensions = {'min':(18,5),'resizable':True, 'align':1}

	def __init__(self,position=(2,20),size=dimensions['min']):
		posx,posy = position
		sizex,sizey = size
		self.wo = curses.newwin(sizey,sizex,posy,posx)
		self.wo.addstr(0,1,self.title,curses.A_STANDOUT)
		for r in self.content:
			r[0] = '0x000000'
			r[1] = curses.A_NORMAL

	def setStart(self,_start):
		self.start = _start

		
	
	def draw(self):
		# round to the nearest 4 bytes
		cols = int(self.sizex/8)
		rows = int(self.sizey-2)
		depth = cols * rows
		rawmem = gb.memory.range_to_list(self.start, depth)
		self.changed = True # temporary measue; needs to be benchmarked first.
		if self.changed:
			self.content = ""
			for r in range(0, rows):
				 for c in range(0,cols):
				 	self.content += hex(rawmem[c*r])
				 self.content += " "
				 for c in range(0,cols/2): # cols is going to be a multiple of 4
				 	self.content += chr(rawmem[c*r]) if rawmem[c*r] >31 and rawmem[c*r] < 127 else "." # experimental NOT  TESTED. (drink time)
				 self.content +="\n"
		self.wo.erase()
		self.wo.addstr(1,1,self.content)
		self.wo.refresh()
			 	

class CodeWindow:
	"""displays the code being executed with highliting"""
	title = "code"
	
	def __init__(self,width,height,posx,posy):
		self.width = width
		self.height = height
		self.posx = posx
		self.posy = posy
		self.wo = curses.newwin(height,width,posy,posx)
		self.wo.addstr(0,2,self.title,curses.A_STANDOUT)
	def draw():
		self.wo
	
	
class ErrorWindow

def display():
	gb.screen.clear()
	gb.screen.addstr(0,0,"testing",curses.A_BOLD)
	for line in gb.output:
		gb.screen.addstr(gb.curline,0,line)
		gb.curline +=1
	gb.screen.refresh()
	
def restorescreen():
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	
	

def drawall():
	#drawregs([('1', 'fffaaa'),('2', '00000000')])
	#drawcode("this is a \n multiline \n \t block \n of code")
	for mem in memoryWindows['visible']:
		mem.draw()
		 
		# mem is a tuple consisting of the memory object and a tuple of 
		# requested range
	
	#drawpreview("and this is a preview of code \n or something..")
	gb.screen.refresh()

#def adjustWindows():
	#gb.screen = curses.initscr()
	
def windowResized():
	sizey,sizex =  gb.screen.getmaxyx()
	minx,miny =  gb.dimensions['min']
	while sizex < minx or sizey < miny:
		screen.clear()
		screen.addstr("crazy fool, that doesn't even fit!")
		try:
			r=(screen.getch())
			c = chr(r)
			if c == 'q':
				quit()
		#except ValueError:
		#	if r == curses.KEY_RESIZE:
				
		except:
			pass
		
		gb.windows['error'].addstr(	"Window too small")
		gb.windows['error'].refresh()
		sizey,sizex = gb.screen.getmaxyx()
	gb.screen.clear()
	setup()
	
def setup():

	code = CodeWindow(20,60,2,10)
	registers = RegistersWindow(32,20,2,70)
	memoryWindows = []
	memoryWindows.append(MemoryWindow(32,6))
	errorWindow = curses.newwin(0,0,2,20)
	
	readCode()	
				
	#gb.windows['error'] = curses.newwin(0,0,2,20)
	#gb.windows['registers'] = [curses.newwin(32,20,2,70),0]
	#gb.windows['registers'][0].border()
	#gb.windows['code'] = [curses.newwin(20,60,2,10),0]
	#gb.windows['code'][0].border()
	#gb.windows['preview'] = [curses.newwin(10,60,24,10),0]
	#gb.windows['preview'][0].border()
	
##TODO clean this up

def readCode():


	f = open(argv[-1])
	prog = f.read()

	output = parser.parse(prog)
	program = simulator.Program()
	program.compile(output)
	#gb.memory = 
	

def main(stdscr):
	screen = stdscr
	curline = 1
	setup()
	curses.noecho()
	curses.cbreak()
	c=''
	while True:
		
		try:
			r=(gb.screen.getch())
			c = chr(r)
		except ValueError:
			if r == curses.KEY_RESIZE:
				windowResized()
				
		if c == 'l':
			display()
		elif c == 'r':
			drawall()
		elif c =='q':
			quit()
		else:
			pass
#	restorescreen()
	print "quittting!"
		
		
curses.wrapper(main)
