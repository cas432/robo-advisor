from app.robo_advisor import threshold_calc
def test_threshold_calc():

    result = threshold_calc(0.10,1000)
    assert result == 1100



