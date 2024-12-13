from collections import defaultdict
import numpy as np
import hashlib


# Find optimal band size using t = (1/b) ^ (1/r)
def find_b_r(num_rows, t):
    min_distance = float('inf')  # Initialize with infinity
    best_r = 2  # Start with default value for r
    best_b = num_rows // 2  # Default b is num_rows / 2

    for i in np.arange(0, 20):  # Iterate over i from 0 to 10
        n = num_rows - i
        for r in range(2, 100):  # Iterate over r from 1 to 100
            if n % r == 0:  # Only consider cases where n is divisible by r
                b = n // r  # Compute b
                distance = abs((1 / b) ** (1 / r) - t)  # Calculate the distance to threshold

                if distance < min_distance:  # Update best values if closer to target
                    min_distance = distance
                    best_r = r
                    best_b = b

    n = int(best_b * best_r)
    return best_b, best_r, n


# Apply LSH with determined b and r and updated n
def apply_lsh(signature_matrix, r, n):
    # Update signature matrix to fit size as determined by best_b and best_r
    signature_matrix = signature_matrix[:n]
    _, cols = signature_matrix.shape
    candidates = set()
    b = n // r
    for band in range(b):
        band_buckets = defaultdict(list)
        for product in range(cols):
            # Hash based on the sequence of band rows
            band_rows = signature_matrix[band * r:(band + 1) * r, product]
            # Place product in unique bucket
            band_hash = hashlib.sha1(band_rows.tobytes()).hexdigest()
            band_buckets[band_hash].append(product)
        for band_hash, bucket_indices in band_buckets.items():
            if len(bucket_indices) > 1:  # Ensure at least two products are in the bucket
                candidates.update((min(i, j), max(i, j)) for i in bucket_indices for j in bucket_indices if i != j)
    total_possible_comparisons = (cols * (cols - 1)) / 2
    fraction_of_comparisons = len(candidates) / total_possible_comparisons

    return candidates, fraction_of_comparisons


def evaluate_lsh_performance(true_duplicates, lsh_candidates):
    # Initialize metrics
    true_positives = set(lsh_candidates) & set(true_duplicates)
    pq = len(true_positives) / len(lsh_candidates) if lsh_candidates else 0
    pc = len(true_positives) / len(true_duplicates)
    f1_star = (2 * pq * pc) / (pq + pc) if pq + pc > 0 else 0
    if pq + pc <= 0: print("pq+pc <= 0")

    return pq, pc, f1_star
