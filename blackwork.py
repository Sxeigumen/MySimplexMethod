'''
column_count = a.shape[0] + 1
line_count = a.shape[1] + 1
size_of_new_matrix = a.shape[0] * a.shape[1] + b.shape[0] + c.shape[0] + 1
canonical_matrix = np.array(range(size_of_new_matrix), int).reshape(line_count, column_count)
canonical_matrix.fill(0)
print(canonical_matrix)
'''

'''
def fix_unacceptable_solution(resolve_line, x_mat = [], poor_matrix=np.array([])):
    resolve_column = -1
    for i in range(0, poor_matrix.shape[0]):
        if poor_matrix[i][resolve_line] < 0:
            resolve_column = i
    x_mat = change_x_matrix(resolve_line, resolve_column, x_mat)
    return x_mat
'''

"""
a = np.array([[2, 1, 1],
              [1, 4, 0],
              [0, 0.5, 1]])

b = np.array([4, 3, 6])

c = np.array([8, 6, 2])

d = do_matrix_in_canonical_form(a, b, c)
"""

"""
while True:
    for i in d.shape[1]:
        if d[i][0] < 0:

"""


'''
def do_matrix_in_canonical_form(flag, matrix_a=np.array([]), matrix_b=np.array([]), matrix_c=np.array([])):
    column_count = matrix_a.shape[0] + 1
    line_count = matrix_a.shape[1] + 1
    size_of_new_matrix = a.shape[0] * a.shape[1] + b.shape[0] + c.shape[0] + 1
    canonical_matrix = np.array(range(size_of_new_matrix), float).reshape(line_count, column_count)

    for lines in range(0, line_count - 1):
        for place in range(0, column_count):
            if place == 0:
                canonical_matrix[lines][place] = matrix_b[lines]
            else:
                canonical_matrix[lines][place] = matrix_a[lines][place - 1]
    if flag == "min":
        for lower_place in range(0, column_count):
            if lower_place == 0:
                canonical_matrix[line_count - 1][lower_place] = 0
            else:
                canonical_matrix[line_count - 1][lower_place] = -(matrix_c[lower_place - 1])
        return canonical_matrix
    if flag == "max":
        for lower_place in range(0, column_count):
            if lower_place == 0:
                canonical_matrix[line_count - 1][lower_place] = 0
            else:
                canonical_matrix[line_count - 1][lower_place] = matrix_c[lower_place - 1]
        return canonical_matrix
'''