import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

class FileMixin:
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class PrettyPrintMixin:
    def __str__(self):
        rows = [' '.join(f"{item:5}" for item in row) for row in self.data]
        return "\n".join(rows)

class AccessMixin:
    def __init__(self):
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        arr = np.array(value)
        if arr.ndim != 2:
            raise ValueError("Matrix data must be 2-dimensional")
        self._data = arr

class Matrix(NDArrayOperatorsMixin, FileMixin, PrettyPrintMixin, AccessMixin):
    def __init__(self, data):
        super(AccessMixin).__init__()
        self.data = data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x._data if isinstance(x, Matrix) else x for x in inputs)
        if 'out' in kwargs:
            kwargs['out'] = tuple(x._data if isinstance(x, Matrix) else x for x in kwargs['out'])
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if isinstance(result, np.ndarray):
            return Matrix(result)
        else:
            return result

if __name__ == '__main__':
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    matrix_add = matrix1 + matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    matrix_add.to_file("artifacts/task2-matrix+.txt")
    matrix_mul.to_file("artifacts/task2-matrix*.txt")
    matrix_matmul.to_file("artifacts/task2-matrix@.txt")
