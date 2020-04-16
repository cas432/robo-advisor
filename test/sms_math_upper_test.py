from app.robo_advisor import sms_math_upper
def test_sms_math_upper():

    result = sms_math_upper(0.05,100)
    assert result == 105
