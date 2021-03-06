from itertools import tee

import numpy as np


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def find_discontinuities(tt, factor=10000):
    """
    Find discontinuities in a timeseries. Returns the indices before each discontinuity.
    """
    dt = np.diff(tt)
    before_jumps = np.where(dt > np.median(dt) * factor)[0]

    if len(before_jumps):
        out = np.array([tt[0], tt[before_jumps[0]]])
        for i, j in pairwise(before_jumps):
            out = np.vstack((out, [tt[i + 1], tt[j]]))
        out = np.vstack((out, [tt[before_jumps[-1] + 1], tt[-1]]))
        return out
    else:
        return np.array([[tt[0], tt[-1]]])


def isin_single_interval(tt, tbound, inclusive_left, inclusive_right):
    if inclusive_left:
        left_condition = (tt >= tbound[0])
    else:
        left_condition = (tt > tbound[0])

    if inclusive_right:
        right_condition = (tt <= tbound[1])
    else:
        right_condition = (tt < tbound[1])

    return left_condition & right_condition


def isin_time_windows(tt, tbounds, inclusive_left=True, inclusive_right=False):
    """
    util: Is time inside time window(s)?
    :param tt:      n,    np.array   time counter
    :param tbounds: k, 2  np.array   time windows
    :return:        n, bool          logical indicating if time is in any of the windows
    """
    # check if tbounds in np.array and if not fix it
    tbounds = np.array(tbounds)
    tt = np.array(tt)

    tf = np.zeros(tt.shape, dtype='bool')

    if len(tbounds.shape) is 1:
        tf = isin_single_interval(tt, tbounds, inclusive_left, inclusive_right)
    else:
        for tbound in tbounds:
            tf = tf | isin_single_interval(tt, tbound, inclusive_left, inclusive_right)
    return tf.astype(bool)