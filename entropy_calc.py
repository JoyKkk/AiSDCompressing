import math
import matplotlib.pyplot as plt
from collections import Counter
from final_report_gen import bwt_encode_block, mtf_encode

def calculate_entropy(data, symbol_size_bytes=1):
    symbols = [data[i:i + symbol_size_bytes] for i in range(0, len(data), symbol_size_bytes)]
    total_symbols = len(symbols)
    counts = Counter(symbols)
    entropy = 0.0
    for count in counts.values():
        p = count / total_symbols
        entropy -= p * math.log2(p)
    return entropy

def plot_entropy_graph(filename, block_sizes):
    with open(f"data/{filename}", "rb") as f:
        data = f.read()

    results = []

    for block_size in block_sizes:
        blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
        transformed_data = bytearray()

        for block in blocks:
            if len(block) == 0:
                continue

            bwt_block = bwt_encode_block(block)
            mtf_block = mtf_encode(bwt_block)
            transformed_data.extend(mtf_block)

        entropy = calculate_entropy(bytes(transformed_data), symbol_size_bytes=1)
        results.append(entropy)
        print(f"Block size {block_size}: Entropy = {entropy:.4f} bits/byte")

    plt.figure(figsize=(8, 5))
    plt.plot(block_sizes, results, marker='o', linestyle='-', color='b')
    plt.title(f"Зависимость энтропии от размера блока ({filename})")
    plt.xlabel("Размер блока (байт)")
    plt.ylabel("Энтропия (бит на байт)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    block_sizes = [256, 512, 1024, 2048, 4096, 8192]
    plot_entropy_graph("enwik7.txt", block_sizes)