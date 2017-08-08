class Command(object):
    def __call__(self, ptr, data_ptr, data, output, input, code):
        self.ptr = ptr 
        self.data_ptr = data_ptr 
        self.data = data 
        self.output = output 
        self.input = input 
        self.code = code

        self.execute()

        return (self.ptr, self.data_ptr, self.data, self.output, self.input)

    def execute(self):
        pass

class increment(Command):
    def execute(self):
        self.data_ptr += 1
        if(self.data_ptr not in self.data):
            self.data[self.data_ptr] = 0

class decrement(Command):
    def execute(self):
        self.data_ptr -= 1
        if(self.data_ptr not in self.data):
            self.data[self.data_ptr] = 0

class increment_data(Command):
    def execute(self):
        if not self.data_ptr in self.data:
            self.data[self.data_ptr] = 0
        if(self.data[self.data_ptr] == 255):
            self.data[self.data_ptr] = 0
        else:
            self.data[self.data_ptr] += 1

class decrement_data(Command):
    def execute(self):
        if not self.data_ptr in self.data:
            self.data[self.data_ptr] = 0
        if(self.data[self.data_ptr] == 0):
            self.data[self.data_ptr] = 255
        else:
            self.data[self.data_ptr] -= 1

class add(Command):
    def execute(self):
        self.data[self.data_ptr] = ord(self.input[0])
        self.input = self.input[1:]

class output(Command):
    def execute(self):
        self.output += chr(self.data[self.data_ptr])

class if_cmd(Command):
    def execute(self):
        if not self.data[self.data_ptr]:
            d = 0
            self.ptr += 1
            while True:
                if(self.code[self.ptr] == "["):
                    d += 1
                if(self.code[self.ptr] == "]"):
                    if not d:
                        break
                    else:
                        d -= 1
                self.ptr += 1

class while_cmd(Command):
    def execute(self):
        if self.data[self.data_ptr]:
            d = 0
            self.ptr -= 1
            while True:
                if(self.code[self.ptr] == "]"):
                    d += 1
                if(self.code[self.ptr] == "["):
                    if not d:
                        break
                    else:
                        d -= 1
                self.ptr -= 1

def interpret(cmd):
    return {
        ">": increment(),
        "<": decrement(),
        "+": increment_data(),
        "-": decrement_data(),
        ".": output(),
        ",": add(),
        "[": if_cmd(),
        "]": while_cmd()
    }[cmd]

def brain_luck(code, input):
    ptr = 0
    data_ptr = 0
    data = {}
    output = ""
    while ptr < len(code):
        command = interpret(code[ptr])
        (ptr, data_ptr, data, output, input) = command(ptr, data_ptr, data, output, input, code) 
        ptr += 1
    return output

def test():
    print brain_luck(',+[-.,+]', 'Codewars' + chr(255)) ==  'Codewars'
    print brain_luck(',[.[-],]', 'Codewars' + chr(0)) == 'Codewars'
    print brain_luck(',>,<[>[->+>+<<]>>[-<<+>>]<<<-]>>.', chr(8) + chr(9)) == chr(72)
    print brain_luck('++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.',"")

if __name__ == '__main__':
    test()