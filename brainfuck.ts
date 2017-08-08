class Interpreter {

    private code_ptr = 0
    private data_ptr = 0
    private data: { [key: number]: number } = {}
    private ostream = ""

    constructor(private code: string, private instream: string) { }

    run() {
        for (; this.code_ptr < this.code.length; ++this.code_ptr) {
            this.interpret(this.code[this.code_ptr]);
        }
        return this.ostream;
    }

    interpret(command) {
        switch (command) {
            case ">": this.increment();
            case "<": this.decrement();
            case "+": this.increment_data();
            case "-": this.decrement_data();
            case ".": this.output();
            case ",": this.add();
            case "[": this.if_cmd();
            case "]": this.while_cmd();
        }
    }

    increment() {
        this.data_ptr++;
    }

    decrement() {
        this.data_ptr--;
    }

    increment_data() {
        if (!(this.data_ptr in this.data)) this.data[this.data_ptr] = 0
        this.data[this.data_ptr] = ++this.data[this.data_ptr] % 256;
    }

    decrement_data() {
        if (!(this.data_ptr in this.data)) this.data[this.data_ptr] = 0
        this.data[this.data_ptr] = --this.data[this.data_ptr] % 256;
    }

    output() {
        this.ostream += String.fromCharCode(this.data[this.data_ptr]);
    }

    add() {
        this.data[this.data_ptr] = this.instream[0] && this.instream[0].charCodeAt(0) || 0;
        this.instream = this.instream.substr(1);
    }

    if_cmd() {
        if (this.data[this.data_ptr]) return;
        this.code_ptr++;
        for (let d = 0; d || this.code[this.code_ptr] != "]"; this.code_ptr++) {
            if (this.code[this.code_ptr] == "[") {
                d++;
            } else if (d) {
                d--;
            }
        }
    }

    while_cmd() {
        if (!this.data[this.data_ptr]) return;
        this.code_ptr--;
        for (let d = 0; d || this.code[this.code_ptr] != "["; this.code_ptr--) {
            if (this.code[this.code_ptr] == "]") {
                d++;
            } else if (d) {
                d--;
            }
        }
    }
}

export function brainLuck(code: string, input: string) {
    const interpreter = new Interpreter(code, input);
    return interpreter.run();
}
