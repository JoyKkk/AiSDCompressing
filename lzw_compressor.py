import math
import matplotlib.pyplot as plt
from collections import Counter

def lzw_encode(data, max_dict_size=4096):
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
    est_size = len(compressed) * 1.5
    print(f"Оригинал: {len(data)} байт")
    print(f"Сжатое: {est_size:.0f} байт")
    print(f"Коэф. сжатия: {len(data)/est_size:.2f}")

    dict_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
    ratios = []
    for dsize in dict_sizes:
        comp = lzw_encode(data, max_dict_size=dsize)
        sz = len(comp) * 1.5
        ratio = len(data) / sz
        ratios.append(ratio)
        print(f"Размер словаря: {dsize:5d} -> коэф. сжатия: {ratio:.2f}")

    plt.figure(figsize=(8, 5))
    plt.plot(dict_sizes, ratios, marker='o', linestyle='-')
    plt.xlabel("Размер словаря (макс. кол-во записей)")
    plt.ylabel("Коэффициент сжатия")
    plt.title("Зависимость коэффициента сжатия LZW от размера словаря")
    plt.grid(True)
    plt.show()