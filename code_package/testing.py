import pytest
from cartesian_robot_module import forced_response
from ads_communication_module import search_index_nextStep, search_index_lastStep, put_array_chronologically, select_useful_data
import numpy as np



#@pytest.mark.parametrize("lastCounter,nextIndex", [(1, 3), (2, 4), (0, 3), (-1, 'NoIndexFound')])
a = [6,7,8,2,3,4,5]                     
def test_search_index_nextStep():
    
    assert search_index_nextStep(a, 1) == 3
    assert search_index_nextStep(a, 2) == 4
    assert search_index_nextStep(a, 0) == 3
    assert search_index_nextStep(a, -1) == 'NoIndexFound'
    missing = 2
    assert search_index_nextStep(a, -1, missing) == 3


def test_search_index_lastStep():
    assert search_index_lastStep(a) == 2

@pytest.mark.parametrize("firstI,lastI,sorted", [(3,2,[2,3,4,5,6,7,8]), (4,6,[3,4,5]), (2,2,[8])])
def test_put_array_chronologically(firstI,lastI,sorted):
    assert np.all(put_array_chronologically(a, firstI, lastI)) == np.all(sorted)




test_time = 0
if test_time == 1:
    import time

    listA = [*range(50,500,1)] + [*range(3,50,1)]
    starting_time = time.time()
    for e in listA:
        search_index_nextStep(listA, e-1)
    print(time.time()-starting_time)
    print(listA)