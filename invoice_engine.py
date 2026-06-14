def process_transaction(raw_reference, amount):
    if raw_reference is None:
        raise ValueError("Missing Client Reference data!")

    clean_text = raw_reference.strip().replace(".", "").upper()
    noise_makers = ["-", "_", ".", "#", "/", ")", "("]

    for char in noise_makers:
        clean_text = clean_text.replace(char, "")

    if amount >= 1000000:
        category = "ENTERPRISE PRIORITIZED"
    else:
        category = "STANDARD ACCOUNTS"
    return clean_text, category

if __name__ == "__main__":
    print("Testing Automation Router engine")
    text1, cat1 = process_transaction(None, 1000000)
    print(f"Cleaned Text: {text1} | Routing target: {cat1}")


