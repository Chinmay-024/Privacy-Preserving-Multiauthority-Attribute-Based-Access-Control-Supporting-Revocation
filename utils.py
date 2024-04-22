import json
import numpy as np

def str_to_matrix(matrix_string):
    """
    Converts a string representation of a matrix back to a matrix (list of lists).
    
    Args:
        matrix_string (str): The string representation of the matrix.
        
    Returns:
        list of lists: The matrix represented as a list of lists.
    """
    # Split the matrix string into rows
    rows = matrix_string.split('\n')
    
    # Convert each row string to a list of elements
    matrix = [row.split(',') for row in rows]
    
    # Convert the elements from strings to the appropriate data types
    matrix = [[int(elem) for elem in row] for row in matrix]
    
    return matrix

def bytes_from_matrix(matrix):
    """
    Converts a matrix (represented as a list of lists) into a string.
    
    Args:
        matrix (list of lists): The input matrix.
        
    Returns:
        str: The matrix represented as a string.
    """
    # Join the rows of the matrix into a single string
    matrix_string = '\n'.join([','.join(map(str, row)) for row in matrix])
    
    return bytes(matrix_string, encoding="utf-8")


def make_square_matrix(A):
    """
    Converts a matrix A of random size into a square matrix by padding it with zeros.
    
    Args:
    A (list of lists): The input matrix.
    
    Returns:
    list of lists: The square matrix.
    """
    # Determine the maximum number of rows and columns
    max_rows = max(len(row) for row in A)
    max_rows = max(len(A), max_rows)
    max_cols = max_rows
    
    # Create a new square matrix and fill it with zeros
    square_matrix = [[0 for _ in range(max_cols)] for _ in range(max_rows)]
    
    # Copy the elements of the input matrix into the square matrix
    for i in range(len(A)):
        for j in range(len(A[i])):
            square_matrix[i][j] = A[i][j]
    
    return square_matrix

# def find_c(A3):
#     # Define the matrix A
#     # r=len(A)
#     A2=make_square_matrix(A3)
#     A = np.array(A2)    
#     target = np.zeros(len(A))
#     target[0] = 1
#     #print(target)
#     # Solve for vector c
#     c = np.linalg.solve(A.T, target)
#     return c

def find_c(A3):
    """
    Solve the linear system Ax = target using the pseudoinverse.
    
    Args:
    A (numpy.ndarray): The coefficient matrix.
    target (numpy.ndarray): The target vector.
    
    Returns:
    numpy.ndarray: The solution vector.
    """
    A2=make_square_matrix(A3)
    #print(A2)
    A = np.array(A2)    
    target = np.zeros(len(A))
    target[0] = 1
    c = np.linalg.pinv(A.T) @ target
    #print("c--:",c)
    return c

def extendedEuclid(a, b):
    if a == 0:
        return b, 0, 1
    gcd, y1, x1 = extendedEuclid(b % a, a)
    x = x1 - (b // a) * y1
    y = y1
    return gcd, x, y


def inverse(a, p):
    if a < 0:
        return p - inverse(-a, p)
    (gcd, x, y) = extendedEuclid(a, p)
    return x % p


def my_object_hook(obj):
    from ECC import Point,curve
    # #print("object    --------- ",obj)
    for key, value in obj.items():
        if isinstance(value, dict) and 'x' in value and 'y' in value:            
            obj[key] = Point((value['x'], value['y']),curve)
            # #print('hi-------------------------',obj[key],value['x'],value['y'])
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict) and 'x' in value[0] and 'y' in value[0]:
            obj[key] = [Point((p['x'], p['y']),curve) for p in value]
        elif isinstance(value, str) and key.endswith('_binary'):
            obj[key] = value.encode('utf-8')
    # #print("***hello",obj)
    return obj

def decode_json_to_data(json_str):
    return json.loads(json_str, object_hook=my_object_hook)

def my_default(obj):
    from ECC import Point
    if isinstance(obj, Point):
        return {'x': obj.x, 'y': obj.y}
    elif isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], Point):
        return [{'x': p.x, 'y': p.y} for p in obj]
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return obj

def encode_data_to_json(data):
    return json.dumps(data, default=my_default)


# Function to multiply a vector and a matrix
def vector_multiplication(sigma1,sigma2,c):
    result1=0
    result2=0
    for i in range(len(sigma1)):
        result1 += sigma1[i] * c[i]
        result2 += sigma2[i] * c[i]
        
    return {'result1':result1, 'result2':result2}
    # Check if the number of elements in the vector matches the number of rows in the matrix
    
