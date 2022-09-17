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