import re

# Separate regex for model words in title or in value
TITLE_MODEL_WORD_REGEX = r'[a-zA-Z0-9]*(?:[0-9]+[^0-9, ]+|[^0-9, ]+[0-9]+)[a-zA-Z0-9]*'
KEY_VALUE_MODEL_WORD_REGEX = r'\d+(?:\.\d+)?[a-zA-Z]+$|^\d+(?:\.\d+)?$'


def extract_title_model_words(text):
    return set(re.findall(TITLE_MODEL_WORD_REGEX, text))


def extract_key_value_model_words(text):
    # Find model words in values
    matches = set(re.findall(KEY_VALUE_MODEL_WORD_REGEX, text))

    # Clean up matches
    cleaned_model_words = []
    for word in matches:
        # Extract numeric parts as string
        cleaned_word = re.sub(r'[a-zA-Z]+', "", word)
        cleaned_model_words.append(cleaned_word)
    return set(cleaned_model_words)

def find_all_model_words(products):
    title_model_words = set()
    key_value_model_words = set()

    for product in products:
        # Extract from titles
        title_model_words.update(extract_title_model_words(product['title']))
        # Extract from key-value pairs
        for value in product['attributes'].values():
            key_value_model_words.update(extract_key_value_model_words(value))

    # Print for visual inspection
    print("title model words:", len(title_model_words), title_model_words)
    print("key value model words:", len(key_value_model_words), key_value_model_words)
    return title_model_words | key_value_model_words


def generate_binary_vectors(products, all_model_words):
    binary_vectors = []

    # Collect model words for all products
    for product in products:
        product_model_words = set()

        # Add model words from the title of the product
        product_model_words.update(extract_title_model_words(product['title']))
        # Add (cleaned) model words from the attribute values of the product
        for attr in product['attributes'].values():
            product_model_words.update(extract_key_value_model_words(attr))

        # Create a binary vector for the current product
        vector = []
        for mw in all_model_words:
            if mw in extract_title_model_words(product['title']) or \
                    any(mw in extract_key_value_model_words(value) for value in product['attributes'].values()):
                vector.append(1)
            else:
                vector.append(0)
        # Combine all products' binary vectors
        binary_vectors.append(vector)

    return binary_vectors
