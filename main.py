import numpy as np


def change_resolve_element(resolve_elem):
    return 1 / resolve_elem


def change_resolve_line_elements(resolve_elem, true_elem):
    return true_elem / resolve_elem


def change_resolve_column_elements(resolve_elem, true_elem):
    return -(true_elem / resolve_elem)


def change_independent_elem(resolve_elem, true_elem, line_elem, column_elem):
    return true_elem - (line_elem * column_elem) / resolve_elem


def change_x_matrix(resolve_line, resolve_column, x_mat=[]):
    tmp_var = x_mat[0][resolve_column]
    x_mat[0][resolve_column] = x_mat[1][resolve_line]
    x_mat[1][resolve_line] = tmp_var
    return x_mat


def do_matrix_in_canonical_form(matrix_a=np.array([]), matrix_b=np.array([]), matrix_c=np.array([])):
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
    for lower_place in range(0, column_count):
        if lower_place == 0:
            canonical_matrix[line_count - 1][lower_place] = 0
        else:
            canonical_matrix[line_count - 1][lower_place] = -(matrix_c[lower_place - 1])
    print(canonical_matrix)
    return canonical_matrix


def define_resolve_parts(resolve_line, poor_matrix=np.array([])):
    resolve_column = -1
    for i in range(0, poor_matrix.shape[0]):
        if poor_matrix[i][resolve_line] < 0:
            resolve_column = i
    return [resolve_line, resolve_column]


def change_simplex_table(res_parts, old_matrix=np.array([])):

    new_matrix = old_matrix.copy()
    resolve_elem = old_matrix[res_parts[0]][res_parts[1]]

    new_matrix[res_parts[0]][res_parts[1]] = change_resolve_element(resolve_elem)

    for i in range(res_parts[0] - 1, -1, -1):
        if res_parts[0] == 0:
            break
        true_elem = old_matrix[i][res_parts[1]]
        new_matrix[i][res_parts[1]] = change_resolve_column_elements(resolve_elem, true_elem)

    for i in range(res_parts[0] + 1, old_matrix.shape[1]):
        if res_parts[0] == old_matrix.shape[1] - 1:
            break
        true_elem = old_matrix[i][res_parts[1]]
        new_matrix[i][res_parts[1]] = change_resolve_column_elements(resolve_elem, true_elem)

    for i in range(res_parts[1] - 1, -1, -1):
        if res_parts[1] == 0:
            break
        true_elem = old_matrix[res_parts[0]][i]
        new_matrix[res_parts[0]][i] = change_resolve_line_elements(resolve_elem, true_elem)

    for i in range(res_parts[1] + 1, old_matrix.shape[0]):
        if res_parts[1] == old_matrix.shape[0] - 1:
            break
        true_elem = old_matrix[res_parts[0]][i]
        new_matrix[res_parts[0]][i] = change_resolve_line_elements(resolve_elem, true_elem)

    for i in range(0, old_matrix.shape[0]):
        if i == res_parts[1]:
            continue
        for j in range(0, old_matrix.shape[1]):
            if j == res_parts[0]:
                continue
            true_elem = old_matrix[j][i]
            line_elem = old_matrix[j][res_parts[1]]
            column_elem = old_matrix[res_parts[0]][i]
            new_matrix[j][i] = change_independent_elem(resolve_elem, true_elem, line_elem, column_elem)
    print(new_matrix)


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

a = np.array([[1, -2, 1],
              [-2, 1, 0],
              [1, 1, 0]])

b = np.array([2, -2, 5])

c = np.array([-1, 1, 0])

x_matrix = [[0, "x1", "x2"],
            ["x3", "x4", "x5"]]

d = do_matrix_in_canonical_form(a, b, c)

resolve_parts = define_resolve_parts(1, d)
x_matrix = change_x_matrix(resolve_parts[0], resolve_parts[1], x_matrix)

change_simplex_table(resolve_parts, d)
