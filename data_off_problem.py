import numpy as np

a = np.array([[2, 1, 1],
              [1, 4, 0],
              [0, 0.5, 1]])

b = np.array([4, 3, 6])

c = np.array([8, 6, 2])

x_matrix = [["S", "x1", "x2", "x3"],
            ["x4", "x5", "x6"]]

unknown_vars = ["x1", "x2", "x3"]

flag = "max"    # Добавил flag

'''
a = np.array([[-2, -1, 0],
              [-1, -4, -0.5],
              [-1, -0, -1]])

b = np.array([-8, -6, -2])

c = np.array([4, 3, 6])

x_matrix = [[0, "x1", "x2"],
            ["x3", "x4", "x5"]]
'''

'''
a = np.array([[1, -2, 1],
              [-2, 1, 0],
              [1, 1, 0]])

b = np.array([2, -2, 5])

c = np.array([-1, 1, 0])

x_matrix = [[0, "x1", "x2"],
            ["x3", "x4", "x5"]]
            
a = np.array([[1, -2, 1],
              [-2, 1, 0],
              [1, 1, 0]])

b = np.array([2, -2, 5])

c = np.array([-1, 1, 0])
'''

'''
a = np.array([[3, 1, 1],
              [1, 1, 0],
              [0, 0.5, 4]])

b = np.array([5, 2, 6])

c = np.array([7, 4, 3])

x_matrix = [[0, "x1", "x2"],
            ["x3", "x4", "x5"]]
'''