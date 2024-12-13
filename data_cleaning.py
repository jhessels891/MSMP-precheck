import re
def normalize_unit(value):
    value = value.lower()
    # Replace various forms of inches, including quotation marks
    value = re.sub(r'\b(inches| inch| inches|-inch|-inches)\b|"', "inch", value)
    # Replace hertz and variations with hz
    value = re.sub(r"\b(hertz| hz| hertz|-hz|-hertz)\b", "hz", value)
    # Replace pounds and variations with lbs
    value = re.sub(r"\b( lbs|lb| lb|lbs.| lbs.|pounds| pounds)\b", "lbs", value)
    # Replace variations of year with year
    value = re.sub(r"\b( year| years|years)\b", "year", value)
    # Remove mm when used as abbreviation for mm, for consistency
    value = re.sub(r"\b(\d+(\.\d+)?mm| mm)\b", "", value)
    # Replace variations of w (indicating wattage) with w
    value = re.sub(r"\b( w| watt|watt| watts|watts)\b", "w", value)
    value = re.sub(r"\b x \b", "x", value)
    value = re.sub(r"\b( day| days|days)\b", "day", value)
    return value

def clean_product_data(product_data):
    cleaned_data = []
    for model_id, product_variants in product_data.items():
        for product in product_variants:
            # Normalize the title and feature map
            title = normalize_unit(product.get("title", ""))
            features_map = {key: normalize_unit(value) for key, value in product.get("featuresMap", {}).items()}

            # Create cleaned product entry
            cleaned_data.append({"title": title, "attributes": features_map, "shop": product.get("shop"), "url": product.get("url"), "modelID": model_id})

    return cleaned_data
