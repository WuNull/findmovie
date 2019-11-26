#!/usr/bin/env python
from multiprocessing.pool import ThreadPool

import time
def process(i):
    print(i)
    # time.sleep(1)
    return


pool = ThreadPool(processes=20)
pool.map(process, (i for i in ['a','b','c','d']))
pool.close()
