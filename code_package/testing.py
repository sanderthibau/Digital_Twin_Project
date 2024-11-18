import pytest
from cartesian_robot_module import forced_response
from ads_communication_module import search_index_nextStep, select_useful_data

@pytest.mark.parametrize("arrayOfCounters,lastCounter,nextIndex", [([6,7,8,2,3,4,5], 1, 3), ([6,7,8,2,3,4,5], 2, 4), ([6,7,8,2,3,4,5], 0, 3)])
                         
def test_search_index_nextStep(arrayOfCounters, lastCounter, nextIndex):
    assert search_index_nextStep(arrayOfCounters, lastCounter) == nextIndex



#print(search_index_nextStep([6,7,8,2,3,4,5], 1))