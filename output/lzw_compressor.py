def lzw_encode(data, max_dict_size=4096):
    # Initialize dictionary with all 256 bytes
    dictionary = {bytes([i]): i for i in range(256)}
    current_string = b""
    result = []

    for byte in data:
        symbol = bytes([byte])
        combined = current_string + symbol
        if combined in dictionary:
            current_string = combined
        else:
            result.append(dictionary[current_string])
            # Add new pattern to dictionary
            if len(dictionary) < max_dict_size:
                dictionary[combined] = len(dictionary)
            current_string = symbol

    if current_string:
        result.append(dictionary[current_string])
    return result

if __name__ == "__main__":
    with open("data/rus.txt", "rb") as f:
        data = f.read()

    compressed = lzw_encode(data)
    # Each result is an integer index (usually 12 bits),
    # so we estimate size as (length * 1.5 bytes)
    est_size = len(compressed) * 1.5
    print(f"\nLZW Results for Russian Text")
    print(f"Original: {len(data)} bytes")
    print(f"Estimated: {est_size:.0f} bytes")
    print(f"Ratio: {len(data)/est_size:.2f}")