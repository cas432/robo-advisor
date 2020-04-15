from app.robo_advisor import to_usd

def test_to_usd():

    result = to_usd(1223.6)
    assert result == "$1,223.60"
