

# creating array in num py

# import numpy as np 

# # ?using list while creating array??
# # arr = np.array([1,2,3,4])

# # using tuple while creating array
# arr = np.array((1,2,3,4))

# print(arr)
# print(type(arr))



# Dimensions in Arrays

import numpy as np 

# 0-D Arrays
# arr = np.array(1233)

# print(arr)

# 1-D Arrays
# arr = np.array([1,2,5,343,343,5])

# print(arr)


# 2-D Arrays
# arr= np.array([[1,2,3,5,353,4] ,[35235 ,545,45,45,45,2]])

# print(arr)



# Createing  a 3-D array with two 2-D arrays
# arr = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

# print(arr)



# Checking Number of Dimensions?


# a = np.array(42)
# b = np.array([1, 2, 3, 4, 5])
# c = np.array([[1, 2, 3], [4, 5, 6]])
# d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

# print('number of dimensions :',a.ndim)
# print('number of dimensions :',b.ndim)
# print('number of dimensions :',c.ndim)
# print('number of dimensions :',d.ndim) 


# Higher Dimensional Arrays

arr = np.array([1, 2, 3, 4], ndmin=5)

print(arr)
print('number of dimensions :', arr.ndim) 