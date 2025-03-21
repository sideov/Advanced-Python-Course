import numpy as np

class HashMixinWithCache:
    cache = {}

    def __hash__(self):
        """
        Так как мы хотим далее искать коллизию, а на это не хочется тратить много времени, а также
        у нас ограничение только на тривиальную (константную) хэш-функцию, то поступим следующим образом:
        хэш станем вычислять как сумму элементов матрицы - таким образом любые неравные матрицы, которые будут
        совпадать как множества своих элементов будут совпадать и по хэшу
        """
        hash_value = 0
        for row in self.data:
            for item in row:
                hash_value += item
        return int(hash_value)

    def check_cache(self, right) -> (bool, any):
        overall_hash = hash((hash(self), hash(right)))
        if overall_hash in HashMixinWithCache.cache.keys():
            return True, HashMixinWithCache.cache[overall_hash]
        return False, None

    def update_cache(self, right, result):
        overall_hash = hash((hash(self), hash(right)))
        HashMixinWithCache.cache[overall_hash] = result



class Matrix3(HashMixinWithCache):
    def __init__(self, data):
        self.data = np.array(data)
        if self.data.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
        self.shape = self.data.shape

    def __add__(self, other):
        if not isinstance(other, Matrix3):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("Error in add: shapes of matrices are different")
        return Matrix3(self.data + other.data)

    def __mul__(self, other):
        if not isinstance(other, Matrix3):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("Error in mul: shapes of matrices are different")
        return Matrix3(self.data * other.data)

    def __matmul__(self, other, /, use_cache=True):
        if not isinstance(other, Matrix3):
            return NotImplemented
        if use_cache:
            is_cached, value = self.check_cache(other)
            if is_cached:
                return value
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"Error in matmul: shapes of matrices are incompatible (matrix1 shape: {self.shape}, matrix2 shape: {other.shape})")
        result = Matrix3(np.matmul(self.data, other.data))
        if use_cache:
            self.update_cache(other, result)
        return result

    def __str__(self):
        rows = [' '.join(f"{item:5}" for item in row) for row in self.data]
        return "\n".join(rows)


if __name__ == "__main__":
    A = Matrix3(np.array([1,2,3,4]).reshape(2,2))
    B = Matrix3(np.array([5,6,3,9]).reshape(2,2))
    C = Matrix3(np.array([4,1,2,3]).reshape(2,2))
    D = Matrix3(np.array([5,6,3,9]).reshape(2,2))
    AB = A @ B
    CD_real = C.__matmul__(D, use_cache=False)

    with open("artifacts/A.txt", "w") as f:
        f.write(str(A))

    with open("artifacts/B.txt", "w") as f:
        f.write(str(B))

    with open("artifacts/C.txt", "w") as f:
        f.write(str(C))

    with open("artifacts/D.txt", "w") as f:
        f.write(str(D))

    with open("artifacts/AB.txt", "w") as f:
        f.write(str(AB))

    with open("artifacts/CD.txt", "w") as f:
        f.write(str(CD_real))

    with open("artifacts/hash.txt", "w") as f:
        text = (f"hash(AB) = {hash(AB)}\n"
                f"hash(CD) = {hash(CD_real)}\n")
        f.write(text)



