import numpy as np
from collections import defaultdict
from itertools import combinations
from scipy.cluster.hierarchy import linkage, fcluster
from model_words import extract_key_value_model_words
from precheck import *
from tmwm import compute_tmwm_sim

# Calculate the dissimilarity for product pairs
def similarity_algorithm(candidate_pairs, products):
    # Initialize distance matrix
    n = len(products)
    dist = np.zeros((n, n))
    count = 0

    # Create q-grams of keys or values
    def qgrams(s, q=3):
        padded_s = f"{'#' * (q - 1)}{s}{'#' * (q - 1)}"
        return [padded_s[i: i + q] for i in range(len(padded_s) - q + 1)]

    # Compute dissimilarity for a specific pair of products
    def compute_dissimilarity(pi, pj, i, j, mu=0.650):
        # Check if the pair is an LSH-candidate pair
        if (i, j) not in candidate_pairs and (j, i) not in candidate_pairs:
            return 100  # High dissimilarity if not LSH candidate pair

        # Preselection, return high similarity in any of these cases
        if pi['shop'] == pj['shop'] or brand_check(pi, pj) or samekey_diffvalues(pi, pj):
            return 100

        sim, avgSim, w, m = 0, 0, 0, 0  # Initialize similarity, weight, and match count

        # Extract key-value pairs for both products
        KV_Pi = pi["attributes"]
        KV_Pj = pj["attributes"]
        unmatched_keys_i = set(KV_Pi.keys())
        unmatched_keys_j = set(KV_Pj.keys())

        # Match keys using q-gram similarity
        for key_i in KV_Pi.keys():
            for key_j in KV_Pj.keys():
                keySim = len(set(qgrams(key_i)) & set(qgrams(key_j))) / len(set(qgrams(key_i)) | set(qgrams(key_j)))
                if keySim > 0.756:  # gamma = 0.756
                    valueSim = len(set(qgrams(KV_Pi[key_i])) & set(qgrams(KV_Pj[key_j]))) / len(
                        set(qgrams(KV_Pi[key_i])) | set(qgrams(KV_Pj[key_j])))
                    weight = keySim
                    sim += weight * valueSim
                    w += weight
                    m += 1
                    unmatched_keys_i.discard(key_i)
                    unmatched_keys_j.discard(key_j)
        if w > 0:
            avgSim = sim / w

        # Extract and combine unmatched values into sets
        unmatched_values_i = set()
        for key in unmatched_keys_i:
            unmatched_values_i.update(extract_key_value_model_words(KV_Pi[key]))

        unmatched_values_j = set()
        for key in unmatched_keys_j:
            unmatched_values_j.update(extract_key_value_model_words(KV_Pj[key]))

        q_gram_set_i = set()
        for s in unmatched_values_i:
            q_gram_set_i.update(qgrams(s))

        q_gram_set_j = set()
        for s in unmatched_values_j:
            q_gram_set_j.update(qgrams(s))

        mwPerc = len(set(q_gram_set_i) & set(q_gram_set_j)) / len(
                        set(q_gram_set_i) | set(q_gram_set_j)) if q_gram_set_i or q_gram_set_j else 0

        # Extract title words and compute TMWM similarity
        titleSim = compute_tmwm_sim(pi["title"], pj["title"]) # Returns 1 of final Sim

        # Adjust based on title similarity
        if titleSim == -1:
            theta_1 = m / min(len(KV_Pi), len(KV_Pj))
            theta_2 = 1 - theta_1
            hSim = theta_1 * avgSim + theta_2 * mwPerc
        else:
            theta_1 = (1 - mu) * (m / min(len(KV_Pi), len(KV_Pj)))
            theta_2 = 1 - mu - theta_1
            hSim = theta_1 * avgSim + theta_2 * mwPerc + mu * titleSim

        return 1 - hSim

    # Compute pairwise similarity for all products
    for i in range(n):
        for j in range(i + 1, n):
            dist[i, j] = compute_dissimilarity(products[i], products[j], i, j)
            if dist[i, j] == 100: count = count + 1
    dist += dist.T  # Ensure the matrix is symmetric
    print("count: ", count)
    return dist

# Input is distance matrix, output is MSM duplicates. Use to tune epsilon in main function
def clustering(distance_matrix, epsilon):
    n = distance_matrix.shape[0]
    linkage_matrix = linkage(distance_matrix[np.triu_indices(n, k=1)], method="single")
    clusters = fcluster(linkage_matrix, t=epsilon, criterion="distance")

    # Find duplicate pairs within clusters
    def find_duplicate_pairs(clusters, n):
        clustered_products = defaultdict(list)

        # Group products by their cluster IDs
        for product_index in range(n):
            cluster_id = clusters[product_index]
            clustered_products[cluster_id].append(product_index)

        # Find duplicate pairs within clusters
        duplicate_pairs = set()
        for products in clustered_products.values():
            if len(products) > 1:
                duplicate_pairs.update(combinations(sorted(products), 2))

        return duplicate_pairs

    duplicate_pairs_found = find_duplicate_pairs(clusters, n)
    return duplicate_pairs_found