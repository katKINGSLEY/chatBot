import msvcrt
import os
import random 


def index(arr):
    res = []
    i = 0
    for x in arr:
        res.append((i,x))
        i += 1
    return res

def raw_str(s):
    return "\n".join(s.splitlines()[1:])

HEADER = raw_str(r'''


    o-----------------------------------------------------------------o
    |            _______ _____   ______         __                    |
    |           |    |  |     |_|   __ \.-----.|  |_.-----.           |
    |           |       |       |    __/|  -__||   _|  -__|           |
    |           |__|____|_______|___|   |_____||____|_____|           |
    |                                                                 |        
    o-----------------------------------------------------------------o''')
EULA=\
"  Please note that this conversation may be recorded for quality assurance."
TOP = raw_str(r'''
    o-----------------------------------------------------------------o
    |                                                                 |''')
LINE = raw_str(r'''
    |                                                                 |''')
PROMPT = raw_str(r'''
    +-----------------------------------------------------------------+
    |  >                                                              |
    |                                                                 |''')
BOTTOM = raw_str(r'''
    o-----------------------------------------------------------------o''')

POINTER_CHAR = "_"
INPUT_START = PROMPT.find(">") + 1

SCREEN_WIDTH = len(TOP.splitlines()[0])
SCREEN_HEIGHT = 30  


ARROW_KEYS = {b"H": "U", b"P": "D", b"K": "L", b"M": "R"}

class Screen:  
    def __init__(self):
        self.pointer = 1
        self.current = []
        self.chat = []

    def start(self):  
        last = ""      
        while True:
            self.update()
            key = msvcrt.getch()
            #print(key)
            #print(last)
            if key == b'\x03':
                # Keyboard interrupt
                break
            elif last == b'\xe0':
                # Arrow keys, move pointer
                if key == b"K":
                    self.move_pointer(-1)
                elif key == b"M":
                    self.move_pointer(1)
            elif key == b'\x08':
                # Backspace
                self.current.pop(self.pointer-1)
                self.pointer -= 1
            elif key == b'\r':
                # Enter (carriage return)
                self.add_chat(random.choice(["Me","NLPete"]), "".join(self.current))
                self.current.clear()
            elif key != b'\xe0':
                # hopefully keyboard input
                try:
                    if len(self.current) < 59*2-2:
                        self.current.insert(self.pointer, key.decode())
                        self.pointer += 1
                except:
                    print(f"Can't decode {key}")
            last = key

    def add_chat(self, user, msg):
        # chat contains each line
        self.chat.append(user)
        for line in [msg[:59], msg[59:]]:
            if line != "":
                self.chat.append(line)
        self.chat.append("")

    def update(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(HEADER)
        print()
        print(EULA)
        print(TOP)
        self.display_chat()
        self.display_input()
        print(BOTTOM)

    def move_pointer(self, move):
        if (move < 0 and self.pointer > 0)\
        or (move > 0 and self.pointer < 59*2):
            self.pointer += move


    def display_chat(self):
        lines = []
        for i in range(SCREEN_HEIGHT-3):
            lines.append(list(LINE))

        msg_index = len(self.chat)-1
        for line in reversed(lines):
            if msg_index < 0:
                break
            start_pos = 9
            msg = self.chat[msg_index]
            if msg in ["Me", "NLPete"]:
                start_pos = 7

            for i, char in index(msg):
                line[start_pos + i] = char
            msg_index -= 1
        print("\n".join(["".join(l) for l in lines]))


    #TODO: fix bug where _ doesnt wrap to other side
    def display_input(self):
        assert len(self.current) < 59*2-1

        str_len = len(self.current)
        new_str = list(PROMPT)
        offset = 0
        start_pos = INPUT_START
        for i, char in index(self.current):
            if i >= 59:
                start_pos = INPUT_START + 14
            if i == self.pointer:
                offset = 1
                new_str[start_pos + i] = POINTER_CHAR
            new_str[start_pos + i + offset] = char

        if offset == 0:
            pos = start_pos + str_len
            if len(self.current) >= 58:
                pos += 14
            new_str[start_pos + str_len] = POINTER_CHAR


        print("".join(new_str))