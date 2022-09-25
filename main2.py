import math
import numpy as np
from data_off_problem import *


class NoAnswers(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return repr(self.info)


def change_resolve_element(resolve_elem):
    return round(1 / resolve_elem, 3)


def change_resolve_line_elements(resolve_elem, true_elem):
    return round(true_elem / resolve_elem, 3)


def change_resolve_column_elements(resolve_elem, true_elem):
    return -(round(true_elem / resolve_elem, 3))


def change_independent_elem(resolve_elem, true_elem, line_elem, column_elem):
    return round(true_elem - (line_elem * column_elem) / resolve_elem, 3)


def change_x_matrix(resolve_line, resolve_column, x_mat=None):
    if x_mat is None:
        x_mat = []
    tmp_var = x_mat[0][resolve_column]
    x_mat[0][resolve_column] = x_mat[1][resolve_line]
    x_mat[1][resolve_line] = tmp_var
    return x_mat


def do_matrix_in_canonical_form(work_mode, matrix_a=np.array([]), matrix_b=np.array([]), matrix_c=np.array([])):
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
            if work_mode == "min":
                canonical_matrix[line_count - 1][lower_place] = -matrix_c[lower_place - 1]
            if work_mode == "max":
                canonical_matrix[line_count - 1][lower_place] = matrix_c[lower_place - 1]
    return canonical_matrix


def fix_define_resolve_parts(wrong_line, poor_matrix=np.array([])):
    counter = 0 #=============
    resolve_column = -1
    divisions = []
    for i in range(1, poor_matrix.shape[0]):
        if poor_matrix[wrong_line][i] < 0:
            resolve_column = i
            counter += 1
            break
    if counter == 0:    #=============
        return "Error"    #=============
    for i in range(poor_matrix.shape[1] - 1):
        divisions.append(poor_matrix[i][0] / poor_matrix[i][resolve_column])
    div_cop = divisions.copy()
    min_div = min(divisions)
    if min_div < 0:
        while min_div < 0:
            min_div = min(div_cop)
            div_cop.remove(min_div)
    resolve_line = divisions.index(min_div)
    return [resolve_line, resolve_column]


def regular_define_resolve_parts(resolve_column, poor_matrix=np.array([])):
    divisions = []
    for i in range(poor_matrix.shape[1] - 1):
        if poor_matrix[i][resolve_column] == 0:
            continue
        divisions.append(poor_matrix[i][0] / poor_matrix[i][resolve_column])
    div_cop = divisions.copy()
    min_div = min(divisions)
    if min_div < 0:
        while min_div < 0:
            min_div = min(div_cop)
            div_cop.remove(min_div)
    return [divisions.index(min_div), resolve_column]


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
    return new_matrix


def print_table(x_mat=None, matrix=np.array([])):
    if x_mat is None:
        x_mat = []
    dist = find_space_distance(matrix)
    numeration_line = "      "
    for elem in x_mat[0]:
        additional_string = elem + "  " * dist
        numeration_line += additional_string
    print(numeration_line)
    for line in range(0, matrix.shape[1] - 1):
        print(x_mat[1][line], " ", matrix[line])
    print("F   ", matrix[matrix.shape[1] - 1])


def print_result(work_mode, x_mat=None, matrix=np.array([])):
    if x_mat is None:
        x_mat = []
    print("Базис")
    for i in range(len(x_mat[1])):
        if x_mat[1][i] in unknown_vars:
            print(x_mat[1][i] + " = " + str(round(matrix[i][0], 2)))
    for i in range(len(x_mat[0])):
        if x_mat[0][i] in unknown_vars:
            print(x_mat[0][i] + " = 0")
    if work_mode == "max":
        print("F = " + str(round(-matrix[matrix.shape[1] - 1][0], 2)))
    if work_mode == "min":
        print("F = " + str(round(matrix[matrix.shape[1] - 1][0], 2)))


def find_space_distance(matrix=np.array([])):
    length_sum = 0
    for elem in matrix[0]:
        length_sum += len(str(elem))
    return math.trunc(length_sum / (matrix.shape[0] * 1.6))


def revise_incorrect_table(x_mat=None, incorrect_matrix=np.array([])):
    if x_mat is None:
        x_mat = []
    while True:
        counter = 0
        incorrect_line = -1
        for index in range(incorrect_matrix.shape[1] - 1):
            if incorrect_matrix[index][0] < 0:
                incorrect_line = index
                counter += 1

        if incorrect_line == -1:
            break

        try:
            resolve_line_column = fix_define_resolve_parts(incorrect_line, incorrect_matrix)
            if resolve_line_column == "Error":
                raise NoAnswers('Решений не существует!!!')
        except NoAnswers as e:
            print(e)
            return "Error"
        x_mat = change_x_matrix(resolve_line_column[0], resolve_line_column[1], x_mat)
        incorrect_matrix = change_simplex_table(resolve_line_column, incorrect_matrix)
        print(resolve_line_column)
        print_table(x_mat, incorrect_matrix)
        print("==================")
    return [x_mat, incorrect_matrix]


def main_part(work_mode, x_mat=None, main_matrix=np.array([])):
    if x_mat is None:
        x_mat = []
    while True:
        key_line = 0
        for index in range(1, main_matrix.shape[0]):
            if main_matrix[main_matrix.shape[1] - 1][index] > 0:
                key_line = index
                break
        if key_line == 0:
            break
        resolve_parts = regular_define_resolve_parts(key_line, main_matrix)
        x_mat = change_x_matrix(resolve_parts[0], resolve_parts[1], x_mat)
        main_matrix = change_simplex_table(resolve_parts, main_matrix)
        print(resolve_parts)
        print_table(x_mat, main_matrix)
        print("==================")
    print_result(work_mode, x_mat, main_matrix)


def direct_problem(work_mode, x_mat=None, direct_matrix=np.array([])):
    if x_mat is None:
        x_mat = []

    print_table(x_mat, direct_matrix)
    print("==================")

    p = revise_incorrect_table(x_mat, direct_matrix)
    if p == "Error":
        return "Error"

    x_mat = p[0]
    direct_matrix = p[1]

    main_part(work_mode, x_mat, direct_matrix)


def dual_problem(work_mode, x_mat=None, matrix_a=np.array([]), matrix_b=np.array([]), matrix_c=np.array([])):
    if work_mode == "min":
        work_mode = "max"
    else:
        work_mode = "min"

    matrix_a = matrix_a.transpose()
    temp_matrix = matrix_b
    matrix_b = matrix_c
    matrix_c = temp_matrix

    dual_matrix = do_matrix_in_canonical_form(work_mode, matrix_a, matrix_b, matrix_c)
    # print_table(x_mat, dual_matrix)
    # print("==================")
    for line in range(dual_matrix.shape[1] - 1):
        for elem in range(dual_matrix.shape[0]):
            dual_matrix[line][elem] *= -1
    direct_problem(work_mode, x_mat, dual_matrix)


if __name__ == "__main__":
    work_matrix = do_matrix_in_canonical_form(flag, a, b, c)
    direct_problem(flag, x_matrix, work_matrix)
    #dual_problem(flag, x_matrix, a, b, c)
