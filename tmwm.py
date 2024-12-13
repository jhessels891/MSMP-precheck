import re
from difflib import SequenceMatcher
from model_words import extract_title_model_words

def normalized_levenshtein(str1, str2):
    # Computes normalized Levenshtein similarity between two strings
    return SequenceMatcher(None, str1, str2).ratio()


def split_model_word(model_word):
    # Split word into numeric and non-numeric part
    non_numeric = re.sub(r'[0-9]', '', model_word)
    numeric = re.sub(r'[^0-9]', '', model_word)
    return non_numeric, numeric

def avg_lv_sim(model_words1, model_words2):
    numerator, denominator = 0, 0

    for word1 in model_words1:
        for word2 in model_words2:
            non_numeric1, numeric1 = split_model_word(word1)
            non_numeric2, numeric2 = split_model_word(word2)

            # Compare non-numeric parts and ensure numeric parts are identical
            if (normalized_levenshtein(non_numeric1, non_numeric2)) >= 0.5 and numeric1 == numeric2:
                lv_distance = normalized_levenshtein(word1, word2)
                weight = len(word1) + len(word2)
                numerator += (1 - lv_distance) * weight
                denominator += weight

    return numerator / denominator if denominator > 0 else 0


def calc_cosine_sim(a, b):
    words_a, words_b = set(a.split()), set(b.split())
    intersection = len(words_a & words_b)
    norm_a, norm_b = len(words_a) ** 0.5, len(words_b) ** 0.5
    return intersection / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0


def compute_tmwm_sim(title1, title2, alpha=0.602, beta=0.1, delta=0.4, threshold=0.5, epsilon=0):
    # Compute cosine similarity
    cosine_sim = calc_cosine_sim(title1, title2)
    if cosine_sim > alpha:
        return 1

    # Extract model words
    model_words1, model_words2 = extract_title_model_words(title1), extract_title_model_words(title2)

    # Compute average Levenshtein similarity for title words
    avg_lv_similarity = avg_lv_sim(set(title1.split()), set(title2.split()))

    # Combine similarities
    final_sim = beta * cosine_sim + (1 - beta) * avg_lv_similarity

    for word1 in model_words1:
        for word2 in model_words2:
            non_sim = normalized_levenshtein(split_model_word(word1)[0], split_model_word(word2)[0])
            num_sim = normalized_levenshtein(split_model_word(word1)[1], split_model_word(word2)[1])

            # Check for similarities of both non-numeric and numeric parts
            if non_sim > 0.5 and num_sim < 1:
                return -1
            if non_sim > 0.5 and num_sim == 1:
                model_word_sim = avg_lv_sim(model_words1, model_words2)
                return delta * model_word_sim + (1 - delta) * final_sim

    return final_sim if final_sim > epsilon else -1
