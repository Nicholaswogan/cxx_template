
from mypackage import MyClass
import numpy as np

my = MyClass()

my.arr = np.random.rand(10000)

print(my.sum_arr())