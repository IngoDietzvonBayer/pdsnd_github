# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:23:09 2021

@author: Ingo
"""

import functions as uf
import math


scores = [88, 92, 79, 93, 80]

mean = uf.mean(scores)
curved = uf.add_five(scores)

mean_c = uf.mean(curved)

print("Scores:", scores)
print("Original Mean:", mean, " New Mean:", mean_c)

print(__name__)
print(uf.__name__)
