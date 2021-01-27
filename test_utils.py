import pandas as pd
import numpy as np

from utils import *

# mock data

df_part2 = pd.DataFrame({'cohfix': [(0, 0.2), (0.1, 0.2), (0.3, 0), (0, 0.2), (0, 0.2)], \
                         'b': [4, 5, 6, 5.5, 7]})

vect = [0.1, 0.9, 0.4, 0.6, 0.8]

# tests

def test_extract_name_pattern():
    out = extract_name_pattern('a20_4.csv')
    assert out[0] == 20
    assert out[1] == 4
    out = extract_name_pattern('bb20_4.csv', prefix = 'bb')
    assert out[1] == 4

def test_extract_data_from_part2():
    out = extract_data_from_part2(df_part2, 'b', (0,0.2))
    assert out[0] == 4
    out = extract_data_from_part2(df_part2, 'b', (0.2, 0))
    assert out[0] == 4
    assert len(out) == 3

def test_compute_mean_sterr_from_vector():
    out = compute_mean_sterr_from_vector(vect)
    tr_mean, tr_sterr = 0.56, 0.128
    assert np.allclose(np.array(out), [tr_mean, tr_sterr], rtol = 0.01)

def test_get_avg_conditions_part2():
    out = get_avg_conditions_part2(df_part2, 0.1, 0.2, 0.3, column = 'b', control = None)
    assert out['cong_m'] == 5
    assert out['cong_s'] == 0

def test_get_avg_conditions_part2():
    out = get_avg_conditions_part2(df_part2, 0.1, 0.2, 0.3, column = 'b', control = None)
    assert out['cong_m'] == 5
    assert out['cong_s'] == 0

def test_confidence_bootstrap():
    out = confidence_bootstrap([1,2,3,4], [7,8,9,10])
    assert out[0] > 0
    out = confidence_bootstrap([1,2,3,4], [1,2,4,5])
    assert out[0] == 0
    out = confidence_bootstrap([1,2,3,4], [1,2,4,5], two_sided = True)
    assert out[0] <= 0
