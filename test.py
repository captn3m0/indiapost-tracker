from tracker import Tracker
from captcha import solve

t = Tracker()

def test_captcha_solves():
    assert solve("captchas/test/a.png", "Evaluate the Expression") == '6'
    assert solve("captchas/test/b.png", "Enter the First number") == '7'
    assert solve("captchas/test/c.png", "Evaluate the Expression") == '6'
    assert solve("captchas/test/test.gif", "Enter characters as displayed in image") == 'c9a8c2'

def test_e2e_tracking():
    data = t.track("ED123456789IN")
    assert data != None
    assert t.is_saved()

def test_html_parsing():
    with open("fixtures/response.html") as f:
        data = t.parse_html(f.read())
        assert 'events' in data
        assert len(data['events']) > 0
        assert data['events'][0]['office'] == 'Tilak Nagar S.O (West Delhi)(Beat Number :17)'

def test_solve_math_captcha():
    details = {"url": "../DOP.Portal.UILayer/MathCaptcha.aspx?Ran=LUaC2Yz6XXIzjBaEP74NcA==", "instructions": "Evaluate the Expression"}
    result = t.solve_captcha(details)
    print(result)
    assert result == '3'

def test_solve_match_pick_captcha():
    details = {"url": "../DOP.Portal.UILayer/MathCaptcha.aspx?Ran=/tCe5F36KpIIy1pWYJfkNw==", "instructions": "Enter the Fifth number"}
    result = t.solve_captcha(details)
    print(result)
    assert result == '4'
