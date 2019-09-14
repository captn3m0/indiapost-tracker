import os
import re
import tempfile
from calculator.simple import SimpleCalculator
import subprocess
from textcaptcha import TextCaptcha

def parse_instructions(instructions):
    # Enter the First number
    if re.search('number', instructions, re.IGNORECASE):
        index_to_num = ["first", "second", "third", "fourth", "fifth"]
        return ('pick', index_to_num.index(instructions.split(' ')[2].lower()))
    # Evaluate the Expression
    elif re.search('evaluate', instructions, re.IGNORECASE):
        return ('evaluate', None)
    # Enter characters as displayed in image
    else:
        return ('read', None)

def solve(filename, instructions):
    c = SimpleCalculator()
    captcha_type, char_index = parse_instructions(instructions)

    if captcha_type=="evaluate":
        print(filename)
        string = recognize(filename)
        print(string)
        c.run(' '.join(list(string)))
        answer = str(int(c.lcd))
        with open('/tmp/guess.txt', 'w') as f:
            f.write(answer)
        return answer
    elif captcha_type=="pick":
        string = recognize(filename)
        with open('/tmp/guess.txt', 'w') as f:
            f.write(string)
        return string[char_index]
    else:
        c = TextCaptcha(filename)
        return c.solve()

def recognize(filename):
    fp = tempfile.NamedTemporaryFile()
    command = [
        "tesseract", filename, fp.name, "--psm", "11",  "-c", 'tessedit_char_whitelist=1234567890,+-='
    ]
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    with open(fp.name + ".txt", 'r') as file:
        data = file.read().replace('\n', '')
    fp.close()
    os.remove(fp.name + ".txt")
    return data.strip()
