import re

def brand_check(product1, product2):
    brand_list = [
        "Acer", "Admiral", "AGA AB", "Aiwa", "Akai", "Alba", "Amstrad", "Andrea Electronics", "Apex Digital", "Apple",
        "Arcam", "Arise India", "Audiovox", "AWA", "Baird", "Bang & Olufsen", "Beko", "BenQ", "Binatone", "Blaupunkt",
        "BPL", "Brionvega", "Bush", "Canadian General Electric", "CGE", "Changhong", "ChiMei", "Compal Electronics",
        "Conar Instruments", "Continental Edison", "Cossor", "Craig", "Curtis Mathes", "Daewoo", "Dell",
        "Delmonico International Corporation", "DuMont Laboratories", "Durabrand", "Dynatron", "EKCO", "Electrohome",
        "Element Electronics", "Emerson Radio & Phonograph", "EMI", "English Electric", "English Electric Valve Company", "Farnsworth", "Ferguson Electronics", "Ferranti", "Finlux",
        "Fisher ", "Electronics", "Fujitsu", "Funai", "Geloso", "General Electric", "General Electric Company", "GoldStar", "Goodmans Industries",
        "Google", "Gradiente", "Graetz", "Grundig", "Haier", "Hallicrafters", "Hannspree", "Heath Company", "Heathkit",
        "Hinari Domestic Appliances", "Hisense", "Hitachi", "HMV", "Hoffman Television", "Itel", "ITT Corporation",
        "Jensen Loudspeakers", "JVC", "Kenmore", "Kent Television", "Kloss Video", "Kogan", "Kolster-Brandes", "Konka", "Lanix", "Le.com",
        "LG", "Loewe", "Luxor", "Magnavox", "Marantz", "Marconiphone", "Matsui", "Memorex", "Metz", "Micromax",
        "Mitsubishi", "Mivar", "Motorola", "Muntz", "Murphy Radio","NEC", "Nokia", "Nordmende", "Onida", "Orion", "Packard Bell",
        "Panasonic", "Pensonic", "Philco", "Philips", "Pioneer", "Planar Systems", "Polaroid","ProLine", "ProScan", "Pye", "Pyle USA", "Quasar", "RadioShack", "Rauland-Borg", "RCA", "Realistic",
        "Rediffusion", "SABA", "Salora", "Salora International", "Samsung", "Sansui", "Sanyo", "Schneider Electric",
        "Seiki Digital", "Sèleco", "Setchell Carlson", "Sharp", "Siemens", "Skyworth", "Sony", "Soyo", "Stromberg-Carlson", "Supersonic",
        "Sylvania", "Symphonic", "Tandy", "Tatung Company", "TCL", "Technics", "TECO", "Teleavia", "Telefunken",
        "Teletronics", "Thomson", "Thorn Electrical Industries", "Thorn EMI", "Toshiba", "TP Vision", "TPV Technology",
        "United States Television Manufacturing.", "Vestel", "Videocon", "Videoton", "Vizio", "Vu Televisions",
        "Walton", "Westinghouse Electric Corporation", "Westinghouse Electronics", "White-Westinghouse", "Xiaomi",
        "Zanussi", "Zenith Radio", "Zonda"
    ]
    brand_set = {brand.lower() for brand in brand_list}
    # Extract potential brand-related information from titles and attributes
    title1 = product1.get("title", "").lower()
    title2 = product2.get("title", "").lower()

    attributes1 = " ".join(product1.get("attributes", {}).values()).lower()
    attributes2 = " ".join(product2.get("attributes", {}).values()).lower()

    # Combine title and attributes to create searchable text
    combined_text1 = f"{title1} {attributes1}"
    combined_text2 = f"{title2} {attributes2}"
    brand1 = None
    brand2 = None
    # Check for any matching brand keywords in both products
    for brand in brand_set:
        if brand in combined_text1:
            brand1 = brand
        if brand in combined_text2:
            brand2 = brand

    return brand1 != brand2 if brand1 is not None and brand2 is not None else False

# Check whether two products both contain one of these keys, and if so, whether they have the same value.
def samekey_diffvalues(product1, product2):
    attributes1 = product1.get("attributes", {})
    attributes2 = product2.get("attributes", {})

    # To extract the numerical part of a value
    def extract_number(value):
        match = re.search(r'\d+(\.\d+)?', value)
        return float(match.group()) if match else None

    # Brightness (only numerical part)
    if "Brightness" in attributes1 and "Brightness" in attributes2:
        brightness1 = extract_number(attributes1["Brightness"])
        brightness2 = extract_number(attributes2["Brightness"])
        if brightness1 != brightness2 and product1["modelID"] == product2["modelID"]:
            print("BRIGHTNESS PROBLEM!")
        return brightness1 != brightness2 if brightness1 is not None and brightness2 is not None else False

    # Component Video Inputs (only numerical part)
    if "Component Video Inputs" in attributes1 and "Component Video Inputs" in attributes2:
        cvi1 = extract_number(attributes1["Component Video Inputs"])
        cvi2 = extract_number(attributes2["Component Video Inputs"])
        if cvi1 != cvi2 and product1["modelID"] == product2["modelID"]:
            print("COMPONENT VIDEO INPUTS PROBLEM!")
        return cvi1 != cvi2 if cvi1 is not None and cvi2 is not None else False

    # Composite Inputs (only numerical part)
    if "Composite Inputs" in attributes1 and "Composite Inputs" in attributes2:
        comp_input1 = extract_number(attributes1["Composite Inputs"])
        comp_input2 = extract_number(attributes2["Composite Inputs"])
        if comp_input1 != comp_input2 and product1["modelID"] == product2["modelID"]:
            print("COMPOSITE INPUTS PROBLEM!")
        return comp_input1 != comp_input2 if comp_input1 is not None and comp_input2 is not None else False

    # DVI Inputs (only numerical part)
    if "DVI Inputs" in attributes1 and "DVI Inputs" in attributes2:
        dvi1 = extract_number(attributes1["DVI Inputs"])
        dvi2 = extract_number(attributes2["DVI Inputs"])
        if dvi1 != dvi2 and product1["modelID"] == product2["modelID"]:
            print("DVI INPUTS PROBLEM!")
        return dvi1 != dvi2 if dvi1 is not None and dvi2 is not None else False

    # HDMI Inputs (only numerical part)
    if "HDMI Inputs" in attributes1 and "HDMI Inputs" in attributes2:
        hdmi1 = extract_number(attributes1["HDMI Inputs"])
        hdmi2 = extract_number(attributes2["HDMI Inputs"])
        if hdmi1 != hdmi2 and product1["modelID"] == product2["modelID"]:
            print("HDMI INPUTS PROBLEM!")
        return hdmi1 != hdmi2 if hdmi1 is not None and hdmi2 is not None else False

    # ENERGY STAR Qualified (exclude if value is 'Unknown')
    if "ENERGY STAR Qualified" in attributes1 and "ENERGY STAR Qualified" in attributes2:
        if attributes1["ENERGY STAR Qualified"] != attributes2["ENERGY STAR Qualified"] and product1["modelID"] == \
                product2["modelID"]:
            print("ENERGY STAR QUALIFIED PROBLEM!")
        return (attributes1["ENERGY STAR Qualified"] != attributes2["ENERGY STAR Qualified"]) \
            if attributes1["ENERGY STAR Qualified"] != "Unknown" and attributes2["ENERGY STAR Qualified"] != "Unknown" \
            else False

    # Ethernet Port
    if "Ethernet Port" in attributes1 and "Ethernet Port" in attributes2:
        if attributes1["Ethernet Port"] != attributes2["Ethernet Port"] and product1["modelID"] == product2["modelID"]:
            print("ETHERNET PORT PROBLEM!")
        return attributes1["Ethernet Port"] != attributes2["Ethernet Port"]

    # Language Options
    if "Language Options" in attributes1 and "Language Options" in attributes2:
        if attributes1["Language Options"] != attributes2["Language Options"] and product1["modelID"] == product2[
            "modelID"]:
            print("LANGUAGE OPTIONS PROBLEM!")
        return attributes1["Language Options"] != attributes2["Language Options"]

    # Speaker Output Power
    if "Speaker Output Power" in attributes1 and "Speaker Output Power" in attributes2:
        if attributes1["Speaker Output Power"] != attributes2["Speaker Output Power"] and product1["modelID"] == product2["modelID"]:
            print("SPEAKER OUTPUT POWER PROBLEM!")
        return attributes1["Speaker Output Power"] != attributes2["Speaker Output Power"]

    return False
