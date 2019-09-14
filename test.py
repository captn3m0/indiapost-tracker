from tracker import Tracker
from captcha import solve

t = Tracker()

def test_captcha_solves():
    assert solve("captchas/test/a.png", "Evaluate the Expression") == '6'
    assert solve("captchas/test/b.png", "Enter the First number") == '7'
    assert solve("captchas/test/c.png", "Evaluate the Expression") == '6'
    assert solve("captchas/test/test.gif", "Enter characters as displayed in image") == 'c9a8c2'

# def test_numbers_3_4():
#     data = t.track("EO430454377IN")
#     assert data != None
