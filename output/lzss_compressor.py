import matplotlib.pyplot as plt
import os

def lzss_encode(data, window_size):
    i = 0
    output = bytearray()
    while i < len(data):
        match_len = 0
        match_dist = 0

        # Look back in the sliding window
        start = max(0, i - window_size)
        for j in range(start, i):
            length = 0
            # Find the longest match (max 255 bytes)
            while i + length < len(data) and data[j + length] == data[i + length] and length < 255:
                length += 1
            if length > match_len:
                match_len = length
                match_dist = i - j

        # If we found a good match (more than 2 bytes), output a pointer
        if match_len > 2:
            output.append(0)                     # Flag: pointer follows
            # Store distance as two bytes (little-endian)
            output.append(match_dist & 0xFF)     # low byte
            output.append((match_dist >> 8) & 0xFF) # high byte
            output.append(match_len)             # length
            i += match_len
        else:
            output.append(1)                     # Flag: literal follows
            output.append(data[i])               # the byte itself
            i += 1
    return output

def plot_lzss_study(filename):
    # Make sure the file exists; use full path or adjust as needed
    file_path = os.path.join("data", filename)
    try:
        with open(file_path, "rb") as f:
            data = f.read()[:5000]   # use only first 5000 bytes for speed
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    windows = [128, 256, 512, 1024, 2048, 4096]
    ratios = []

    print(f"Investigating LZSS Window Sizes for {filename}...")
    for w in windows:
        compressed = lzss_encode(data, w)
        ratio = len(data) / len(compressed)
        ratios.append(ratio)
        print(f"Window {w}: Ratio {ratio:.2f} (compressed size = {len(compressed)})")

    plt.figure(figsize=(8, 5))
    plt.plot(windows, ratios, marker='s', color='green')
    plt.title("LZSS: Compression Ratio vs Window Size")
    plt.xlabel("Window Size (Bytes)")
    plt.ylabel("Compression Ratio")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_lzss_study("rus.txt")