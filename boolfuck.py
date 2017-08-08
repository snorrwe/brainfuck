class Command(object):
    def init(self, ptr, data_ptr, data, output, input, code):
        self.ptr = ptr 
        self.data_ptr = data_ptr 
        self.data = data 
        self.output = output 
        self.input = input 
        self.code = code

    def __call__(self, ptr, data_ptr, data, output, input, code):
        self.init(ptr, data_ptr, data, output, input, code)
        if(self.data_ptr not in self.data):
            self.data[self.data_ptr] = 0
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
        self.data[self.data_ptr] = 1 - self.data[self.data_ptr]

class add(Command):
    def execute(self):
        if not self.input:
            self.data[self.data_ptr] = 0
            return
        data = [int(x) for x in list('{0:0b}'.format(ord(self.input[0])))]
        for i in data[::-1]:
            self.data[self.data_ptr] = int(i)
            self.data_ptr += 1
        self.data_ptr -= 1
        self.input = self.input[1:]

class output(Command):
    def execute(self):
        self.output.append(self.data[self.data_ptr])

class if_cmd(Command):
    def execute(self):
        print("if", self.ptr, self.data_ptr, self.data[self.data_ptr])
        if self.data[self.data_ptr]:
            return
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
        print("while", self.ptr, self.data_ptr, self.data[self.data_ptr])
        if not self.data[self.data_ptr]:
            return
        d = 0
        self.ptr -= 1
        while True:
            if(self.code[self.ptr] == "]"):
                d += 1
            elif(self.code[self.ptr] == "["):
                if not d:
                    break
                else:
                    d -= 1
            self.ptr -= 1

def interpret(cmd):
    try:
        return {
            ">": increment(),
            "<": decrement(),
            "+": increment_data(),
            ";": output(),
            ",": add(),
            "[": if_cmd(),
            "]": while_cmd()
        }[cmd]
    except KeyError:
        return lambda ptr, data_ptr, data, output, input, code: (ptr, data_ptr, data, output, input)

def print_stream(output):
    result = ""
    diff = len(output) % 8
    for i in range(diff):
        output.append(0)
    for i, n in enumerate(output[::-8]):
        sum = 0
        for j, bit in enumerate(output[i*8:i*8+7]):
            if bit:
                sum += pow(2, j)
        result += chr(sum)
    print (result)
    return result

def boolfuck(code, input=""):
    ptr = 0
    data_ptr = 0
    data = {}
    output = []
    while ptr < len(code):
        command = interpret(code[ptr])
        (ptr, data_ptr, data, output, input) = command(ptr, data_ptr, data, output, input, code) 
        ptr += 1
    return print_stream(output)

def test():
    print(boolfuck(";;;+;+;;+;+;+;+;+;+;;+;;+;;;+;;+;+;;+;;;+;;+;+;;+;+;;;;+;+;;+;;;+;;+;+;+;;;;;;;+;+;;+;;;+;+;;;+;+;;;;+;+;;+;;+;+;;+;;;+;;;+;;+;+;;+;;;+;+;;+;;+;+;+;;;;+;+;;;+;+;+;", "") == "Hello, world!\n")
    print(boolfuck(";asd;;asd+asf;adf+sda;fsd;gd+ghdg;hg+df;+;+;+;+;;+;;+;;;+;;+;+;;+;;;+;;+;+;;+;+;;;;+;+;;+;;;+;;+;+;+;;;;;;;+;+;;+;;;+;+;;;+;+;;;;+;+;;+;;+;+;;+;;;+;;;+;;+;+;;+;;;+;+;;+;;+;+;+;;;;+;+;;;+;+;+;", "") == "Hello, world!\n")
    print(boolfuck(">,>,>,>,>,>,>,>,<<<<<<<[>]+<[+<]>>>>>>>>>[+]+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<;>;>;>;>;>;>;>;<<<<<<<,>,>,>,>,>,>,>,<<<<<<<[>]+<[+<]>>>>>>>>>[+]+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]", "Codewars\u00ff") == "Codewars")
    print(boolfuck(">,>,>,>,>,>,>,>,>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>;>;>;>;>;>;>;>;>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]>,>,>,>,>,>,>,>,>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]", "Codewars") == "Codewars")

if __name__ == '__main__':
    test()