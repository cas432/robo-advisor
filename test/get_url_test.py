from app.robo_advisor import get_url
import json

def test_get_url():

    response = get_url("d","N9PA30F4N9P35ETT")
    keys = json.loads(response.text).keys()

    assert "Meta Data" in keys
    assert "Time Series (Daily)" in keys

