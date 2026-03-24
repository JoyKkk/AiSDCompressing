import os
import time
from collections import Counter
from rle_compressor import rle_encode
from lzss_compressor import lzss_encode
from lzw_compressor import lzw_encode
import heapq

# --- 1. HUFFMAN MODULE ---
class HuffmanNode:
    def __init__(self, char, freq):
        self.char, self.freq, self.left, self.right = char, freq, None, None
    def __lt__(self, other): return self.freq < other.freq

def huff_encode(data):
    if not data: return 0
    counts = Counter(data)
    heap = [HuffmanNode(c, f) for c, f in counts.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
        merged = HuffmanNode(None, n1.freq + n2.freq)
        merged.left, merged.right = n1, n2
        heapq.heappush(heap, merged)
    codes = {}
    def get_codes(n, c):
        if n.char is not None: codes[n.char] = c
        else:
            get_codes(n.left, c+"0"); get_codes(n.right, c+"1")
    get_codes(heap[0], "")
    bits = sum(len(codes[b]) for b in data)
    return (bits + 7) // 8

# --- 2. RLE MODULE ---
def rle_size(data, Ms=8):
    s_bytes = Ms // 8
    size = 0; i = 0
    while i < len(data):
        run = 1
        while i+run*s_bytes < len(data) and data[i:i+s_bytes] == data[i+run*s_bytes:i+(run+1)*s_bytes] and run < 127: run += 1
        if run > 1: size += 1 + s_bytes; i += run * s_bytes
        else:
            unique = 0
            while i < len(data):
                if i+(2*s_bytes) <= len(data) and data[i:i+s_bytes] == data[i+s_bytes:i+2*s_bytes]: break
                unique += 1; i += s_bytes
                if unique >= 127: break
            size += 1 + (unique * s_bytes)
    return size

# --- 3. BWT/MTF MODULE ---
def bwt_encode_block(data):
    rot = sorted([data[i:] + data[:i] for i in range(len(data))])
    return bytes([r[-1] for r in rot])

def mtf_encode(data):
    alpha = list(range(256))
    res = []
    for b in data:
        idx = alpha.index(b)
        res.append(idx)
        alpha.insert(0, alpha.pop(idx))
    return bytes(res)

# --- 4. LZSS/LZW MODULE ---
def lzss_size(data):
    # Based on your study, we use 4KB window
    i = 0; size = 0
    while i < len(data):
        m_len = 0
        for j in range(max(0, i-4096), i):
            l = 0
            while i+l < len(data) and data[j+l] == data[i+l] and l < 255: l += 1
            m_len = max(m_len, l)
        if m_len > 2: size += 3; i += m_len
        else: size += 2; i += 1
    return size

def lzw_size(data):
    # Using 4096 dict size
    d = {bytes([i]): i for i in range(256)}; s = b""; count = 0
    for b in data:
        char = bytes([b])
        if s + char in d: s += char
        else:
            count += 1
            if len(d) < 4096: d[s+char] = len(d)
            s = char
    return int((count + 1) * 1.5)

# --- FINAL TABLE GENERATOR ---
def run_report():
    files = ["rus.txt", "binary.exe", "enwik7.txt", "bw.raw", "gray.raw", "color.raw"]
    print("\nТаблица коэффициентов сжатия")
    print(f"{'Имя файла':<18} | {'HA':<5} | {'RLE':<5} | {'BWT+RLE':<7} | {'BWT+MTF+HA':<10} | {'BWT+MTF+RLE+HA':<13} | {'LZSS':<5} | {'LZSS+HA':<8} | {'LZW':<5} | {'LZW+HA':<8}")
    print("-" * 112)
 
    for fname in files:
        path = f"data/{fname}"
        if not os.path.exists(path): continue
        with open(path, "rb") as f: raw = f.read()

        # Use a sample for speed on large files
        sample = raw[:20000]
        orig = len(sample)

        # Calculate sizes
        ha = orig / huff_encode(sample)
        rle = orig / rle_size(sample, 24 if "color" in fname else 8)

        # BWT Block process
        bwt_data = bytearray()
        for i in range(0, len(sample), 2000): # Small blocks for speed
            bwt_data.extend(bwt_encode_block(sample[i:i+2000]))

        bwt_rle = orig / rle_size(bwt_data)
        bwt_mtf_ha = orig / huff_encode(mtf_encode(bwt_data))
        lzss = orig / lzss_size(sample)
        lzw = orig / lzw_size(sample)

        mtf_data = mtf_encode(bwt_data)
        rle_data = rle_encode(mtf_data, 8)
        bwt_mtf_rle_ha = orig / huff_encode(rle_data)

        lzss_data = lzss_encode(sample, 4096)
        lzss_ha = orig / huff_encode(lzss_data)

        lzw_data = lzw_encode(sample, 4096)
        lzw_ha = orig / huff_encode(lzw_data)
 
        print(f"{fname[:18]:<18} | {ha:<5.2f} | {rle:<5.2f} | {bwt_rle:<7.2f} | {bwt_mtf_ha:<10.2f} | {bwt_mtf_rle_ha:<14.2f} | {lzss:<5.2f} | {lzss_ha:<8.2f} | {lzw:<5.2f} | {lzw_ha:<8.2f}")

def run_size_report():
    files = ["rus.txt", "binary.exe", "enwik7.txt", "bw.raw", "gray.raw", "color.raw"]
    print("\nТаблица размеров при разных видах сжатия (в байтах)")
    print(f"{'Имя файла':<18} | {'Исходник':<10} | {'HA':<8} | {'RLE':<8} | {'BWT+RLE':<10} | {'BWT+MTF+HA':<12} | {'BWT+MTF+RLE+HA':<16} | {'LZSS':<8} | {'LZSS+HA':<10} | {'LZW':<8} | {'LZW+HA':<10}")
    print("-" * 145)

    for fname in files:
        path = f"data/{fname}"
        if not os.path.exists(path):
            continue

        with open(path, "rb") as f:
            raw = f.read()

        sample = raw[:20000]
        orig = len(raw)
        scale = len(raw) / len(sample)

        ha = int(huff_encode(sample) * scale)
        rle = int(rle_size(sample, 24 if "color" in fname else 8) * scale)

        bwt_data = bytearray()
        for i in range(0, len(sample), 2000):
            bwt_data.extend(bwt_encode_block(sample[i:i+2000]))

        bwt_rle = int(rle_size(bwt_data) * scale)
        bwt_mtf_ha = int(huff_encode(mtf_encode(bwt_data)) * scale)

        mtf_data = mtf_encode(bwt_data)
        rle_data = rle_encode(mtf_data, 8)
        bwt_mtf_rle_ha = int(huff_encode(rle_data) * scale)

        lzss = int(lzss_size(sample) * scale)

        lzss_data = lzss_encode(sample, 4096)
        lzss_ha = int(huff_encode(lzss_data) * scale)

        lzw = int(lzw_size(sample) * scale)

        lzw_data = lzw_encode(sample, 4096)
        lzw_ha = int(huff_encode(lzw_data) * scale)

        print(f"{fname[:18]:<18} | {orig:<10} | {ha:<8} | {rle:<8} | {bwt_rle:<10} | {bwt_mtf_ha:<12} | {bwt_mtf_rle_ha:<16} | {lzss:<8} | {lzss_ha:<10} | {lzw:<8} | {lzw_ha:<10}")

if __name__ == "__main__":
    run_report()
    # run_size_report()