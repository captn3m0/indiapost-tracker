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
        string = recognize(filename)
        c.run(' '.join(list(string)))
        return int(c.lcd)
    elif captcha_type=="pick":
        string = recognize(filename)
        return string[char_index]
    else:
        c = TextCaptcha(filename)
        return c.solve()

def recognize(filename):
    fp = tempfile.NamedTemporaryFile()
    subprocess.run(["tesseract", filename, fp.name, "--psm", "7",  "-c", 'tessedit_char_whitelist=1234567890,+-='], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(fp.name + ".txt", 'r') as file:
        data = file.read().replace('\n', '')
    # Delete fp.name + ".txt"
    return data.strip()

if __name__ == "__main__":
    print(solve("captchas/test/a.png", "Evaluate the Expression"))
    print(solve("captchas/test/b.png", "Enter the First number"))
    print(solve("captchas/test/c.png", "Evaluate the Expression"))
    print(solve("captchas/test/test.gif", "Enter characters as displayed in image"))

