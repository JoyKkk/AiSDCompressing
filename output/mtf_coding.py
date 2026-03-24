def mtf_encode(data):
    alphabet = list(range(256))
    result = []
    for byte in data:
        idx = alphabet.index(byte)
        result.append(idx)
        pop_byte = alphabet.pop(idx)
        alphabet.insert(0, pop_byte)
    return bytes(result)

def mtf_decode(data):
    alphabet = list(range(256))
    result = []
    for idx in data:
        byte = alphabet[idx]
        result.append(byte)
        pop_byte = alphabet.pop(idx)
        alphabet.insert(0, pop_byte)
    return bytes(result)

if __name__ == "__main__":
    # We import the entropy function from your other file
    from entropy_calc import calculate_entropy

    # Let's test it on the Russian text
    with open("data/rus.txt", "rb") as f:
        original = f.read()

    encoded = mtf_encode(original)

    # Calculate entropy before and after MTF
    h_orig = calculate_entropy(original, 1)
    h_mtf = calculate_entropy(encoded, 1)

    print("\n" + "="*40)
    print(f"Результаты MTF")
    print("-" * 40)
    print(f"Энтропия оригинала: {h_orig:.4f}")
    print(f"Энтропия с MTF: {h_mtf:.4f}")
    print("-" * 40)

    # Check if decompression works
    decoded = mtf_decode(encoded)
    print(f"Совпали данные? {original == decoded}")
    print("="*40 + "\n")