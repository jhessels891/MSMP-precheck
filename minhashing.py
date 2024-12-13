import numpy as np
import random


def generate_minhash_functions(num_hashes, max_value):
    hash_funcs = []
    for _ in range(num_hashes):
        # Each hash function is a permutation, i.e., a random ordering of indices.
        perm = list(range(max_value))
        random.shuffle(perm)
        hash_funcs.append(perm)

    return hash_funcs

def compute_signature_matrix(binary_vectors, num_hashes):
    num_products = len(binary_vectors)
    num_model_words = len(binary_vectors[0])  # Assuming all vectors have the same length
    signature_matrix = np.full((num_hashes, num_products), float('inf'))

    # Generate random permutations (hash functions)
    hash_funcs = generate_minhash_functions(num_hashes, num_model_words)

    for i, vector in enumerate(binary_vectors):
        for j in range(num_hashes):
            # Find the first '1' in the vector for the current permutation
            perm = hash_funcs[j]
            for k in range(num_model_words):
                if vector[perm[k]] == 1:  # Find first '1' under permutation
                    signature_matrix[j, i] = k  # Record the index of the first '1'
                    break  # Stop as soon as the first '1' is found

    print("shape sig matrix na minhashing: ", signature_matrix.shape)
    return signature_matrix.astype(int)
