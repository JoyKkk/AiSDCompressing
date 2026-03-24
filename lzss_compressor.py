import matplotlib.pyplot as plt
import os

def lzss_encode(data, window_size):
    i = 0
    output = bytearray()
    while i < len(data):
        match_len = 0
        match_dist = 0

        start = max(0, i - window_size)
        for j in range(start, i):
            length = 0
            while i + length < len(data) and data[j + length] == data[i + length] and length < 255:
                length += 1
            if length > match_len:
                match_len = length
                match_dist = i - j

        if match_len > 2:
            output.append(0)
            output.append(match_dist & 0xFF)
            output.append((match_dist >> 8) & 0xFF)
            output.append(match_len)
            i += match_len
        else:
            output.append(1)
            output.append(data[i])
            i += 1
    return output

def plot_lzss_study(filename):
    file_path = os.path.join("data", filename)
    try:
        with open(file_path, "rb") as f:
            data = f.read()[:5000]
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return

    windows = [128, 256, 512, 1024, 2048, 4096, 8192, 2**14, 2**15, 2**16]
    ratios = []

    for w in windows:
        compressed = lzss_encode(data, w)
        ratio = len(data) / len(compressed)
        ratios.append(ratio)
        print(f"Окно {w}: Коэф. {ratio:.2f} (размер = {len(compressed)})")

    plt.figure(figsize=(8, 5))
    plt.plot(windows, ratios, marker='s', color='green')
    plt.title("Зависимость коэффициента сжатия от размера буфера")
    plt.xlabel("Размер буфера (байты)")
    plt.ylabel("Коэффициент сжатия")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_lzss_study("rus.txt")