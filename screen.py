import config as cfg
import msvcrt
import os

class Screen:  
    def __init__(self):
        self.pointer = 0
        self.current = []
        self.chat = []
        self.last = ""
        self.user_name = "Me"

    def step(self):  
        key = msvcrt.getch()
        #print(key)
        #print(last)
        if key == b'\x03':
            # Keyboard interrupt
            return "break"
        elif self.last == b'\xe0':
            # Arrow keys, move pointer
            if key == b"K":
                self.move_pointer(-1)
            elif key == b"M":
                self.move_pointer(1)
        elif key == b'\x08':
            # Backspace
            if len(self.current) > 0:
                self.current.pop(self.pointer-1)
                self.pointer -= 1
        elif key == b'\r':
            # Enter (carriage return)
            if len(self.current) > 0:
                msg = "".join(self.current)
                self.add_chat(self.user_name, msg)
                self.current.clear()
                self.pointer = 0
                return msg       
        elif key not in [b'\xe0', b'\t']:
            # hopefully keyboard input
            try:
                if len(self.current) < 59*2-2:
                    self.current.insert(self.pointer, key.decode())
                    self.pointer += 1
            except:
                print(f"Can't decode {key}")
        self.last = key
        return None

    def add_chat(self, user, msg):
        # chat contains each line
        self.chat.append(user)
        last = 0
        for i in range(1,10):
            line = msg[last:last+59]
            if line == "":
                break
            last = last + 59
            self.chat.append(line)
        self.chat.append("")

    def update(self, thinking=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(cfg.HEADER)
        print()
        print(cfg.EULA)
        print(cfg.TOP)
        self.display_chat()
        self.display_input(thinking)
        print(cfg.BOTTOM)

    def move_pointer(self, move):
        if (move < 0 and self.pointer > 0)\
        or (move > 0 and self.pointer < 59*2 and self.pointer < len(self.current)):
            self.pointer += move


    def display_chat(self):
        lines = []
        for i in range(cfg.SCREEN_HEIGHT-3):
            lines.append(list(cfg.LINE))

        msg_index = len(self.chat)-1
        for line in reversed(lines):
            if msg_index < 0:
                break
            start_pos = 9
            msg = self.chat[msg_index]
            if msg in [self.user_name, "NLPete"]:
                start_pos = 7

            for i, char in cfg.index(msg):
                line[start_pos + i] = char
            msg_index -= 1
        print("\n".join(["".join(l) for l in lines]))


    #TODO: fix bug where _ doesnt wrap to other side
    def display_input(self, thinking):
        assert len(self.current) < 59*2-1

        if not thinking:
            str_len = len(self.current)
            new_str = list(cfg.PROMPT)
            offset = 0
            start_pos = cfg.INPUT_START
            for i, char in cfg.index(self.current):
                if i >= 59:
                    start_pos = cfg.INPUT_START + 13
                if i == self.pointer:
                    offset = 1
                    new_str[start_pos + i] = cfg.POINTER_CHAR
                new_str[start_pos + i + offset] = char

            if offset == 0:
                pos = start_pos + str_len
                if len(self.current) >= 58:
                    pos += 13
                new_str[start_pos + str_len] = cfg.POINTER_CHAR
            print("".join(new_str))
        else:
            print(cfg.PROMPT_THINKING)


