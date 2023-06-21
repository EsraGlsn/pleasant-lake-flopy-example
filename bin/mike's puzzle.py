
# %% PACKAGE IMPORTS

import numpy as np

# %% MAIN SCRIPT

# start with a rectangular 2D array

og_arr = np.array([[0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
                   [1, 6, 11, 16, 21, 26, 31, 36, 41, 46],
                   [2, 7, 12, 17, 22, 27, 32, 37, 42, 47],
                   [3, 8, 13, 18, 23, 28, 33, 38, 43, 48],
                   [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]])

# does the for loop below achieve what we want as stated above? What might you
# adjust within the for loops to get the desired array?


### ========= MAKE CHANGES BELOW HERE ========================================

arr = np.zeros((5, 10))
counter = 0
for iii in range(arr.shape[0]):
    for jjj in range(arr.shape[1]):
        arr[iii, jjj] = counter
        counter += 1

### ========= MAKE CHANGES ABOVE HERE ========================================


# let's test to see if they're the same

if (og_arr == arr).all():
    print("Success!!! Congratulations to the for-loop champion!")

else:
    print("no, unfortunately that's not correct...")


### ========= MAKE CHANGES ABOVE HERE ESRA ========================================

esra = np.array([[0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
                [1, 6, 11, 16, 21, 26, 31, 36, 41, 46],
                [2, 7, 12, 17, 22, 27, 32, 37, 42, 47],
                [3, 8, 13, 18, 23, 28, 33, 38, 43, 48],
                [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]])

pot=[]
for i in range(0,50):
    print(i)
    pot.append(i)

print(pot)

pot_np = np.array(pot)
a = pot_np.reshape(10,5)
b = a.T

if (esra == b).all():
    print("Success!!! Congratulations to the for-loop champion!")

else:
    print("no, unfortunately that's not correct...")


### ========= MAKE CHANGES ABOVE HERE AEJ ========================================

j = 5
x, y = np.meshgrid(np.arange(0,50,j), np.arange(j))
aej = x+y

# print('aej:',aej)
# print('eg:', esra)

if (esra == aej).all():
    print("Success!!! Congratulations to the for-loop champion!")

else:
    print("no, unfortunately that's not correct...")




### ========= MAKE CHANGES ABOVE HERE ESRA AND AEJ====================================

import numpy as np
np.arange(0,50).reshape(10,5).T

