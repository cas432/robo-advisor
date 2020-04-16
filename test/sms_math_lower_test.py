from app.robo_advisor import sms_math_lower

def test_sms_math_lower():

    result = sms_math_lower(0.05,100)
    assert result == 95
