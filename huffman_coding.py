import heapq
import sys
import os
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    counts = Counter(data)
    heap = [Node(char, freq) for char, freq in counts.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)
    return heap[0]

def build_codes(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

def huffman_compress(data):
    if not data: return b"", {}
    root = build_huffman_tree(data)
    codes = {}
    build_codes(root, "", codes)

    bit_string = "".join(codes[byte] for byte in data)

    padding = 8 - (len(bit_string) % 8)
    bit_string += "0" * padding

    byte_res = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_res.append(int(bit_string[i:i+8], 2))

    return bytes(byte_res), codes

if __name__ == "__main__":
    with open("data/enwik7.txt", "rb") as f:
        original_data = f.read()
    print("\n" + "="*37)
    print("Сжатие Хаффманом")
    print("-" * 37)

    victim = original_data

    compressed, codes = huffman_compress(victim)

    print(f"Исходный размер: {len(victim)} байт")
    print(f"Сжатый размер: {len(compressed)} байт")

    ratio = len(victim) / len(compressed)
    print(f"Коэф. сжатия: {ratio:.2f}")
    print("="*37 + "\n")