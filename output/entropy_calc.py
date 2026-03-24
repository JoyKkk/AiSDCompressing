import math
import matplotlib.pyplot as plt
from collections import Counter

def calculate_entropy(data, symbol_size_bytes):
    # Break data into symbols of N bytes
    symbols = [data[i : i + symbol_size_bytes] for i in range(0, len(data), symbol_size_bytes)]
    total_symbols = len(symbols)

    # Count how often each symbol appears
    counts = Counter(symbols)

    entropy = 0
    for count in counts.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)

    return entropy

def plot_entropy_graph(filename):
    with open(f"data/{filename}", "rb") as f:
        data = f.read()

    # filter out non-ASCII for the English text test
    # (only keeping bytes < 128)
    filtered_data = bytes([b for b in data if b < 128])

    sizes = [1, 2, 3, 4]
    results = []

    for s in sizes:
        h = calculate_entropy(filtered_data, s)
        # We normalize entropy per byte for the graph
        results.append(h / s)
        print(f"Size {s} byte(s): Entropy = {h:.4f}")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, results, marker='o', linestyle='-', color='b')
    plt.title(f"Entropy vs Symbol Size ({filename})")
    plt.xlabel("Symbol Size (Bytes)")
    plt.ylabel("Entropy (bits per byte)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # English text (enwik7)
    plot_entropy_graph("rus.txt")