"""
Author: Zhan Shi
Time  : 2021/6/6 14:53
"""

import pandas as pd
import phe

from app.src.path import PK_PATH, SK_PATH


def generate_keypair(length):
    """
    Generate keypair
    :param length: keypair length
    """
    (pk, sk) = phe.generate_paillier_keypair(n_length=length)

    pd.DataFrame(data=[str(pk.n)], index=['n']).to_pickle(PK_PATH)
    pd.DataFrame(data=[str(sk.p), str(sk.q)], index=['p', 'q']).to_pickle(SK_PATH)

    return f"·N={hex(pk.n).upper()} \n·P={hex(sk.p).upper()} \n·Q={hex(sk.q).upper()}"
