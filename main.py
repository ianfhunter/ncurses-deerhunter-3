# coding: utf-8
import curses,time,random

faces = [
'''
///\    
||oo    
|| >   
 \_-     
''',
'''
/\'\'\'    
c-OO    
`` >    
 ```     
''',
'''
@@@@    
c oo    
\  ^    
 \_~     
''',
'''
//\'\'
c-oo    
\  ^
 \_-
''',
'''
@@@@    
c ..    
\  7    
 \_v    
''',
'''
/\'\'\'
c-OO
\  z
 \_=
'''
]

script = [
   (
    "\"You kill deer good. Show Grod how.\"",
    [
      ("Sure, I show Grod",2),
      ("Only if Grod catch deer with me",2),
      ("Grod is too stupid to learn.",1),
      ("Learn your own way Grod",1),
    ]
   ),
   (
    "\"That not nice, Grod want to learn\"",
    [
      ("Sure, I show Grod",2),
      ("Only if Grod catch deer with me",2),
      ("Grod is too stupid to learn.",1),
      ("Learn your own way Grod",1),
    ]
   ),
   (
    "\"Oh good! Grod like deer meat\"",
    [
      ("You need to get a heavy rock",3),
      ("You need to get a light rock",3),
      ("You need to be really quiet",3),
      ("I just practised a lot",3),
    ]
   ),
   (
    "\"... Is that it?\"",
    [
      ("Never kill male deer",4),
      ("Detatch the antlers",4),
      ("Cover yourself in deer dung",4),
      ("That's it.",4),
    ]
   ),
    (
    "\"Thank you, Grod will go and try\"",
    [
      ("Good luck hunter",None),
      ("Bring me back some",None),
      ("Just don't die",None),
      ("Bye Grod",None),
    ]
   ),
    (
    "\"Hmpf. Grod is better hunter anyway\"",
    [
      ("Ok, you can leave",None),
      ("Are we done?",None),
      ("Sigh..",None),
      ("Bye Grod",None),
    ]
   ),
]

def conversation(mainwin,window,person,script):
    
    state = 0
    while(state is not None):
        draw_person(window,person,1,0,curses.color_pair(1))
        dwin.border(0)
        dwin.addstr(6, 1, script[state][0],curses.color_pair(5))
        dwin.addstr(8, 1, "A) " +script[state][1][0][0],curses.color_pair(5))
        dwin.addstr(9, 1, "B) " +script[state][1][1][0],curses.color_pair(5))
        dwin.addstr(10, 1, "C) " +script[state][1][2][0],curses.color_pair(5))
        dwin.addstr(11, 1,"D) " +script[state][1][3][0],curses.color_pair(5))
        dwin.refresh()
        res = kbhit(mainwin,['a','b','c','d','A','B','C','D'],[])
        if res != 0 and res != 3 and res != -1:
            val = ord(res) - 97
            state = script[state][1][val][1]  
            dwin.clear()
            dwin.refresh()
            res = 0
    dwin.addstr(1, 1,"DONE",curses.color_pair(5))
    dwin.border(0)
    dwin.refresh()
    dwin.refresh()
    time.sleep(8)
def draw_ascii(window,ascii_art,x,y,attr):
    for line_idx, line in enumerate(ascii_art.splitlines()):
        window.addstr(line_idx + y, x, line,attr)

def draw_person(window,person,x,y,attr):
    draw_ascii(window,person.art,x,y,attr) #border of 1
    window.addstr(y + 1,x + 6,"Name: Grod",attr)
    window.addstr(y + 1,x + 20,"Mood: Disgruntled",attr)
    window.addstr(y + 2,x + 6,"Appearance: Muscular",attr)
    window.addstr(y + 3,x + 6,"STR: " + str(person.attributes["STR"]),attr)
    window.addstr(y + 3,x + 13,"CHA: "+str(person.attributes["CHA"]),attr)
    window.addstr(y + 3,x + 20,"DEX: "+str(person.attributes["DEX"]),attr)
    window.addstr(y + 4,x + 6,"INT: "+ str(person.attributes["INT"]),attr) 
    window.addstr(y + 4,x + 13,"WIS: "+str( person.attributes["WIS"]),attr) 
    window.addstr(y + 4,x + 20,"CON: "+ str(person.attributes["CON"]),attr) 

class Person:
    def __init__(self):
        self.art = getRandomPerson()
        self.attributes = {
          "WIS":random.randint(0,6),
          "CON":random.randint(0,6),
          "STR":random.randint(0,6),
          "INT":random.randint(0,6),
          "DEX":random.randint(0,6),
          "CHA":random.randint(0,6),
        }

def getRandomPerson():
    face = faces[random.randint(0,len(faces) -1)]
    return face

def kbhit(window,char,no):
    ch = window.getch();
    if ch == -1:
        return 0

    try:
        nch = int(str(chr(ch)))
    except ValueError:
        nch = -1

    cch = chr(ch)

    if (cch in char or nch in no):
        if (cch in char):
            curses.ungetch(ch)
            curses.flushinp()
            return cch
        else:
            return 2
    else:
        return 3

body = '''
:-)
'''

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(1)

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)


stdscr.border(0)
stdscr.refresh()

dWidth = 40
dHeight = 40

#lines, columns,  beginX, beginY
dwin = curses.newwin(dHeight, dWidth, 1,1)
hintwin = curses.newwin(dWidth,40, 1,dWidth + 1)

dwin.clear()
dwin.border(0)

grod = Person()

conversation(stdscr,dwin,grod,script)


dwin.refresh()

# Power Bars
hintwin.border(0)
hintwin.refresh()


stdscr.nodelay(1)

#dwin.addstr(1, 1,"Result is" + str(res))   
dwin.refresh()
time.sleep(8)



curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
