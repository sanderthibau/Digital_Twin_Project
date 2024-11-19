import pytest
from cartesian_robot_module import forced_response
from ads_communication_module import search_index_nextStep, select_useful_data

@pytest.mark.parametrize("arrayOfCounters,lastCounter,nextIndex", [([6,7,8,2,3,4,5], 1, 3), ([6,7,8,2,3,4,5], 2, 4), ([6,7,8,2,3,4,5], 0, 3), ([6,7,8,3,4,5], 0, 'NoIndexFound')])
                         
def test_search_index_nextStep(arrayOfCounters, lastCounter, nextIndex):
    assert search_index_nextStep(arrayOfCounters, lastCounter) == nextIndex





test_time = 0
if test_time == 1:
    import time

    listA = [*range(50,500,1)] + [*range(3,50,1)]
    starting_time = time.time()
    for e in listA:
        search_index_nextStep(listA, e-1)
    print(time.time()-starting_time)
    print(listA)