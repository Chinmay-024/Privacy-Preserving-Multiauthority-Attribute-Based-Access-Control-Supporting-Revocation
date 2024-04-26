# Function to multiply two vectors
def vector_multiplication(vector1, vector2):
    # Check if the vectors have the same length
    if len(vector1) != len(vector2):
        return "Vectors must have the same length"
    
    # Initialize the result vector
    result = [0] * len(vector1)
    
    # Multiply the corresponding elements of the vectors
    for i in range(len(vector1)):
        result[i] = vector1[i] * vector2[i]
    
    return result

# Example usage
vector_C = [1, 2, 3]  # Input vector
vector_sigma = [4, 5, 6]  # Input vector

result = vector_multiplication(vector_C, vector_sigma)

if isinstance(result, list):
    #print("Result of vector multiplication:")
    #print(result)
else:
    #print(result)