import math
import numpy as np
from data_off_problem import *


class NoAnswers(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return repr(self.info)


class SimplexMethodComponents(object):

    @staticmethod
    def change_resolve_element(resolveElem):
        return round(1 / resolveElem, 3)

    @staticmethod
    def change_resolve_line_elements(resolveElem, trueElem):
        return round(trueElem / resolveElem, 3)

    @staticmethod
    def change_resolve_column_elements(resolveElem, trueElem):
        return -(round(trueElem / resolveElem, 3))

    @staticmethod
    def change_independent_elem(resolveElem, trueElem, lineElem, columnElem):
        return round(trueElem - (lineElem * columnElem) / resolveElem, 3)

    @staticmethod
    def change_x_matrix(resolveLine, resolveColumn, xMat=None):
        if xMat is None:
            xMat = []
        tmp_var = xMat[0][resolveColumn]
        xMat[0][resolveColumn] = xMat[1][resolveLine]
        xMat[1][resolveLine] = tmp_var
        return xMat

    @staticmethod
    def do_matrix_in_canonical_form(workMode, matrixA=np.array([]), matrixB=np.array([]), matrixC=np.array([])):
        columnCount = matrixA.shape[0] + 1
        lineCount = matrixA.shape[1] + 1
        sizeOfNewMatrix = a.shape[0] * a.shape[1] + b.shape[0] + c.shape[0] + 1
        canonicalMatrix = np.array(range(sizeOfNewMatrix), float).reshape(lineCount, columnCount)

        for lines in range(0, lineCount - 1):
            for place in range(0, columnCount):
                if place == 0:
                    canonicalMatrix[lines][place] = matrixB[lines]
                else:
                    canonicalMatrix[lines][place] = matrixA[lines][place - 1]

        for lowerLinesElem in range(0, columnCount):
            if lowerLinesElem == 0:
                canonicalMatrix[lineCount - 1][lowerLinesElem] = 0
            else:
                if workMode == "min":
                    canonicalMatrix[lineCount - 1][lowerLinesElem] = -matrixC[lowerLinesElem - 1]
                if workMode == "max":
                    canonicalMatrix[lineCount - 1][lowerLinesElem] = matrixC[lowerLinesElem - 1]
        return canonicalMatrix

    @staticmethod
    def fix_define_resolve_parts(wrongLine, poorMatrix=np.array([])):
        counter = 0  # =============
        resolveColumn = -1
        divisions = []
        for elem in range(1, poorMatrix.shape[0]):
            if poorMatrix[wrongLine][elem] < 0:
                resolveColumn = elem
                counter += 1
                break
        if counter == 0:  # =============
            return "Error"  # =============
        for elem in range(poorMatrix.shape[1] - 1):
            divisions.append(poorMatrix[elem][0] / poorMatrix[elem][resolveColumn])
        divCopy = divisions.copy()
        minDiv = min(divisions)
        if minDiv < 0:
            while minDiv < 0:
                minDiv = min(divCopy)
                divCopy.remove(minDiv)
        resolveLine = divisions.index(minDiv)
        return [resolveLine, resolveColumn]

    @staticmethod
    def regular_define_resolve_parts(resolveColumn, poorMatrix=np.array([])):
        divisions = []
        for i in range(poorMatrix.shape[1] - 1):
            if poorMatrix[i][resolveColumn] == 0:
                continue
            divisions.append(poorMatrix[i][0] / poorMatrix[i][resolveColumn])
        divCopy = divisions.copy()
        minDiv = min(divisions)
        if minDiv < 0:
            while minDiv < 0:
                minDiv = min(divCopy)
                divCopy.remove(minDiv)
        return [divisions.index(minDiv), resolveColumn]

    @staticmethod
    def change_simplex_table(resolveLineNColumn, oldMatrix=np.array([])):
        newMatrix = oldMatrix.copy()
        resolveElem = oldMatrix[resolveLineNColumn[0]][resolveLineNColumn[1]]

        newMatrix[resolveLineNColumn[0]][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_element(
            resolveElem)

        for elem in range(resolveLineNColumn[0] - 1, -1, -1):
            if resolveLineNColumn[0] == 0:
                break
            trueElem = oldMatrix[elem][resolveLineNColumn[1]]
            newMatrix[elem][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_column_elements(resolveElem,
                                                                                                            trueElem)

        for elem in range(resolveLineNColumn[0] + 1, oldMatrix.shape[1]):
            if resolveLineNColumn[0] == oldMatrix.shape[1] - 1:
                break
            trueElem = oldMatrix[elem][resolveLineNColumn[1]]
            newMatrix[elem][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_column_elements(resolveElem,
                                                                                                            trueElem)

        for elem in range(resolveLineNColumn[1] - 1, -1, -1):
            if resolveLineNColumn[1] == 0:
                break
            trueElem = oldMatrix[resolveLineNColumn[0]][elem]
            newMatrix[resolveLineNColumn[0]][elem] = SimplexMethodComponents.change_resolve_line_elements(resolveElem,
                                                                                                          trueElem)

        for elem in range(resolveLineNColumn[1] + 1, oldMatrix.shape[0]):
            if resolveLineNColumn[1] == oldMatrix.shape[0] - 1:
                break
            trueElem = oldMatrix[resolveLineNColumn[0]][elem]
            newMatrix[resolveLineNColumn[0]][elem] = SimplexMethodComponents.change_resolve_line_elements(resolveElem,
                                                                                                          trueElem)

        for elem in range(0, oldMatrix.shape[0]):
            if elem == resolveLineNColumn[1]:
                continue
            for line in range(0, oldMatrix.shape[1]):
                if line == resolveLineNColumn[0]:
                    continue
                trueElem = oldMatrix[line][elem]
                line_elem = oldMatrix[line][resolveLineNColumn[1]]
                column_elem = oldMatrix[resolveLineNColumn[0]][elem]
                newMatrix[line][elem] = SimplexMethodComponents.change_independent_elem(resolveElem, trueElem, line_elem,
                                                                                        column_elem)
        return newMatrix


class PrintForSimplexMethod(object):
    @staticmethod
    def find_space_distance(matrix=np.array([])):
        lengthSum = 0
        for elem in matrix[0]:
            lengthSum += len(str(elem))
        return math.trunc(lengthSum / (matrix.shape[0] * 1.6))

    @staticmethod
    def print_table(xMat=None, matrix=np.array([])):
        if xMat is None:
            xMat = []
        dist = PrintForSimplexMethod.find_space_distance(matrix)
        numerationLine = "      "
        for elem in xMat[0]:
            additionalString = elem + "  " * dist
            numerationLine += additionalString
        print(numerationLine)
        for line in range(0, matrix.shape[1] - 1):
            print(xMat[1][line], " ", matrix[line])
        print("F   ", matrix[matrix.shape[1] - 1])

    @staticmethod
    def print_result(workMode, xMat=None, matrix=np.array([])):
        if xMat is None:
            xMat = []
        print("Базис")
        for i in range(len(xMat[1])):
            if xMat[1][i] in unknown_vars:
                print(xMat[1][i] + " = " + str(round(matrix[i][0], 2)))
        for i in range(len(xMat[0])):
            if xMat[0][i] in unknown_vars:
                print(xMat[0][i] + " = 0")
        if workMode == "max":
            print("F = " + str(round(-matrix[matrix.shape[1] - 1][0], 2)))
        if workMode == "min":
            print("F = " + str(round(matrix[matrix.shape[1] - 1][0], 2)))


class MainActions(object):

    @staticmethod
    def revise_incorrect_table(xMat=None, incorrectMatrix=np.array([])):
        if xMat is None:
            xMat = []
        while True:
            counter = 0
            incorrectLine = -1
            for index in range(incorrectMatrix.shape[1] - 1):
                if incorrectMatrix[index][0] < 0:
                    incorrectLine = index
                    counter += 1

            if incorrectLine == -1:
                break

            try:
                resolveLineColumn = SimplexMethodComponents.fix_define_resolve_parts(incorrectLine, incorrectMatrix)
                if resolveLineColumn == "Error":
                    raise NoAnswers('Решений не существует!!!')
            except NoAnswers as e:
                print(e)
                return "Error"
            xMat = SimplexMethodComponents.change_x_matrix(resolveLineColumn[0], resolveLineColumn[1], xMat)
            incorrectMatrix = SimplexMethodComponents.change_simplex_table(resolveLineColumn, incorrectMatrix)
            print(resolveLineColumn)
            PrintForSimplexMethod.print_table(xMat, incorrectMatrix)
            print("==================")
        return [xMat, incorrectMatrix]

    @staticmethod
    def main_part(workMode, xMat=None, mainMatrix=np.array([])):
        if xMat is None:
            xMat = []
        while True:
            keyLine = 0
            for index in range(1, mainMatrix.shape[0]):
                if mainMatrix[mainMatrix.shape[1] - 1][index] > 0:
                    keyLine = index
                    break
            if keyLine == 0:
                break
            resolveLineNColumn = SimplexMethodComponents.regular_define_resolve_parts(keyLine, mainMatrix)
            xMat = SimplexMethodComponents.change_x_matrix(resolveLineNColumn[0], resolveLineNColumn[1], xMat)
            mainMatrix = SimplexMethodComponents.change_simplex_table(resolveLineNColumn, mainMatrix)
            print(resolveLineNColumn)
            PrintForSimplexMethod.print_table(xMat, mainMatrix)
            print("==================")
        PrintForSimplexMethod.print_result(workMode, xMat, mainMatrix)


class TypeOfProblem(object):
    @staticmethod
    def direct_problem(workMode, xMat=None, directMatrix=np.array([])):
        if xMat is None:
            xMat = []

        PrintForSimplexMethod.print_table(xMat, directMatrix)
        print("==================")

        correctMatrix = MainActions.revise_incorrect_table(xMat, directMatrix)
        if correctMatrix == "Error":
            return "Error"

        xMat = correctMatrix[0]
        directMatrix = correctMatrix[1]

        MainActions.main_part(workMode, xMat, directMatrix)

    @staticmethod
    def dual_problem(workMode, xMat=None, matrixA=np.array([]), matrixB=np.array([]), matrixC=np.array([])):
        if workMode == "min":
            workMode = "max"
        else:
            workMode = "min"

        matrixA = matrixA.transpose()
        tempMatrix = matrixB
        matrixB = matrixC
        matrixC = tempMatrix

        dual_matrix = SimplexMethodComponents.do_matrix_in_canonical_form(workMode, matrixA, matrixB, matrixC)
        for line in range(dual_matrix.shape[1] - 1):
            for elem in range(dual_matrix.shape[0]):
                dual_matrix[line][elem] *= -1
        TypeOfProblem.direct_problem(workMode, xMat, dual_matrix)


if __name__ == "__main__":
    d_matrix = SimplexMethodComponents.do_matrix_in_canonical_form(flag, a, b, c)
    TypeOfProblem.direct_problem(flag, x_matrix, d_matrix)
    #TypeOfProblem.dual_problem(flag, x_matrix, a, b, c)
