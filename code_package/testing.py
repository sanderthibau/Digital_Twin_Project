import pytest
from cartesian_robot_module import forced_response
from ads_communication_module import search_index_nextStep, search_index_lastStep, put_array_chronologically, select_useful_data
import numpy as np
from collections import OrderedDict



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

od = OrderedDict([('aDataCounter', [41, 42, 43, 44, 45, 46, 37, 38, 39, 40]), 
                 ('aTime', [40000000, 41000000, 42000000, 43000000, 44000000, 45000000, 36000000, 37000000, 38000000, 39000000])])
prev_count = 37

#@pytest.mark.parametrize()
def test_select_useful_data():

    useful_counter = select_useful_data(od, prev_count)['aDataCounter']
    assert np.all(useful_counter) == np.all([38, 39, 40, 41, 42, 43, 44, 45, 46])

    useful_time = select_useful_data(od, prev_count)['aTime']
    assert np.all(useful_time) == np.all([37000000, 38000000, 39000000, 40000000, 41000000, 42000000, 43000000, 44000000, 45000000])
                  




test_time = 0
if test_time == 1:
    import time

    listA = [*range(50,500,1)] + [*range(3,50,1)]
    starting_time = time.time()
    for e in listA:
        search_index_nextStep(listA, e-1)
    print(time.time()-starting_time)
    print(listA)