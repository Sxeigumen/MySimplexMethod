import math
import numpy as np
from data_off_problem import *


class WorkWithBasicMatrix(object):
    @staticmethod
    def redactingBasicMatrix(matrixCondition=None, matrixA=np.array([]), matrixB=np.array([])):
        if matrixCondition is None:
            matrixCondition = []
        for index in range(len(matrixCondition)):
            if matrixCondition[index] == '>=':
                matrixB[index] = matrixB[index] * (-1)
                for elem in range(matrixA.shape[0]):
                    matrixA[index][elem] = matrixA[index][elem] * (-1)
        return [matrixA, matrixB]

    @staticmethod
    def createUnknownVarsMatrix(matrixC=np.array([])):
        variables = []
        for index in range(matrixC.shape[0]):
            variables.append(f'x{index + 1}')
        return variables

    @staticmethod
    def createXMatrix(matrixCondition=None, matrixC=np.array([])):
        xM = []
        tempMatrix = []
        if matrixCondition is None:
            matrixCondition = []
        for index in range(matrixC.shape[0]):
            if index == 0:
                tempMatrix.append('S')
            tempMatrix.append(f'x{index + 1}')
        xM.append(tempMatrix.copy())
        tempMatrix.clear()
        for index in range(len(matrixCondition)):
            tempMatrix.append(f'x{index + 1 + matrixC.shape[0]}')
        xM.append(tempMatrix.copy())
        tempMatrix.clear()
        return xM


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
        tmpVar = xMat[0][resolveColumn]
        xMat[0][resolveColumn] = xMat[1][resolveLine]
        xMat[1][resolveLine] = tmpVar
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
        counter = 0
        resolveColumn = -1
        divisionResults = []
        for elem in range(1, poorMatrix.shape[0]):
            if poorMatrix[wrongLine][elem] < 0:
                resolveColumn = elem
                counter += 1
                break
        if counter == 0:
            print("?????? ??????????????")
            exit(0)
        for elem in range(poorMatrix.shape[1] - 1):
            divisionResults.append(poorMatrix[elem][0] / poorMatrix[elem][resolveColumn])
        divCopy = divisionResults.copy()
        minDiv = min(divisionResults)
        if minDiv < 0:
            while minDiv < 0:
                minDiv = min(divCopy)
                divCopy.remove(minDiv)
        resolveLine = divisionResults.index(minDiv)
        return [resolveLine, resolveColumn]

    @staticmethod
    def regular_define_resolve_parts(resolveColumn, poorMatrix=np.array([])):
        divisionResults = []

        for i in range(poorMatrix.shape[1] - 1):
            if poorMatrix[i][resolveColumn] == 0:
                continue
            divisionResults.append(poorMatrix[i][0] / poorMatrix[i][resolveColumn])

        divisionResultsCopy = divisionResults.copy()
        minDivisionResult = min(divisionResults)

        if minDivisionResult < 0:
            while minDivisionResult < 0:
                if len(divisionResultsCopy) == 0:
                    print("?????????????? ???????????????????? ??????????!")
                    exit(0)
                minDivisionResult = min(divisionResultsCopy)
                divisionResultsCopy.remove(minDivisionResult)

        return [divisionResults.index(minDivisionResult), resolveColumn]

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
                newMatrix[line][elem] = SimplexMethodComponents.change_independent_elem(resolveElem, trueElem,
                                                                                        line_elem,
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
        unknownVars = WorkWithBasicMatrix.createUnknownVarsMatrix(c)
        print("??????????")
        for i in range(len(xMat[1])):
            if xMat[1][i] in unknownVars:
                print(xMat[1][i] + " = " + str(round(matrix[i][0], 2)))
        for i in range(len(xMat[0])):
            if xMat[0][i] in unknownVars:
                print(xMat[0][i] + " = 0")
        if workMode == "max":
            print("F = " + str(round(-matrix[matrix.shape[1] - 1][0], 2)))
        if workMode == "min":
            print("F = " + str(round(matrix[matrix.shape[1] - 1][0], 2)))


class MainActions(object):
    @staticmethod
    def revisingIncorrectTable(xMat=None, incorrectMatrix=np.array([])):
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

            resolveLineColumn = SimplexMethodComponents.fix_define_resolve_parts(incorrectLine, incorrectMatrix)
            xMat = SimplexMethodComponents.change_x_matrix(resolveLineColumn[0], resolveLineColumn[1], xMat)
            incorrectMatrix = SimplexMethodComponents.change_simplex_table(resolveLineColumn, incorrectMatrix)
            print(resolveLineColumn)
            PrintForSimplexMethod.print_table(xMat, incorrectMatrix)
            print("==================")
        return [xMat, incorrectMatrix]

    @staticmethod
    def optimizingSolution(workMode, xMat=None, mainMatrix=np.array([])):
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

        correctMatrix = MainActions.revisingIncorrectTable(xMat, directMatrix)

        xMat = correctMatrix[0]
        directMatrix = correctMatrix[1]

        MainActions.optimizingSolution(workMode, xMat, directMatrix)

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
    xMatrix = WorkWithBasicMatrix.createXMatrix(condition, c)
    newMatrix = WorkWithBasicMatrix.redactingBasicMatrix(condition, a, b)
    a = newMatrix[0]
    b = newMatrix[1]
    directMatrix = SimplexMethodComponents.do_matrix_in_canonical_form(flag, a, b, c)
    PrintForSimplexMethod.print_table(xMatrix, directMatrix)
    print("===================")
    TypeOfProblem.dual_problem(flag, xMatrix, a, b, c)
