import numpy as np


class Matrix:
    def __init__(self, data):
        self.data = np.array(data)
        if self.data.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
        self.shape = self.data.shape

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("Error in add: shapes of matrices are different")
        return Matrix(self.data + other.data)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("Error in mul: shapes of matrices are different")
        return Matrix(self.data * other.data)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"Error in matmul: shapes of matrices are incompatible (matrix1 shape: {self.shape}, matrix2 shape: {other.shape})")
        return Matrix(np.matmul(self.data, other.data))

    def __str__(self):
        rows = [' '.join(f"{item:5}" for item in row) for row in self.data]
        return "\n".join(rows)


if __name__ == "__main__":
    np.random.seed(0)
    matrix1_data = np.random.randint(0, 10, (10, 10))
    matrix2_data = np.random.randint(0, 10, (10, 10))

    matrix1 = Matrix(matrix1_data)
    matrix2 = Matrix(matrix2_data)

    matrix_add = matrix1 + matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    with open("artifacts/matrix+.txt", "w") as f:
        f.write(str(matrix_add))

    with open("artifacts/matrix*.txt", "w") as f:
        f.write(str(matrix_mul))

    with open("artifacts/matrix@.txt", "w") as f:
        f.write(str(matrix_matmul))
