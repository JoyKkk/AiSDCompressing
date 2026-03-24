import os
import time
from collections import Counter
import matplotlib.pyplot as plt
from utils import read_bitstring_from_file, write_bitstring_to_file
from entropy import entropy
from mtf import mtf_encode, mtf_decode
from huffman import huffman_encode, huffman_decode
from bwt import bwt, inverse_bwt, build_suffix_array
from lz77 import lzss_encode, lzss_decode
from lz78 import lzw_encode, lzw_decode
from compressors import *

# ------------------- Тестовые файлы -------------------
test_files = {
    'enwik7': 'test_data/enwik7',
    'russian.txt': 'test_data/russian.txt',
    'binary.exe': 'test_data/binary.exe',
    'bw_image.raw': 'test_data/bw_image.raw',
    'gray_image.raw': 'test_data/gray_image.raw',
    'color_image.raw': 'test_data/color_image.raw'
}

# ------------------- Задание 1: RLE -------------------
def test_rle():
    for name, path in test_files.items():
        with open(path, 'rb') as f:
            data = f.read()
        # RLE с Ms=8, Mc=8
        enc = rle_encode(data, 8, 8)
        dec = rle_decode(enc, 8, 8)
        assert dec == data, f"RLE failed for {name}"
        ratio = len(enc) / len(data) if len(data) > 0 else 1
        print(f"{name}: RLE ratio = {ratio:.3f}")

# ------------------- Задание 2: Энтропия, MTF, Хаффман, BWT -------------------
def entropy_study():
    # возьмём английский текст (например, enwik7)
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    # фильтруем символы >127 (ASCII)
    data_ascii = bytes(b for b in data if b < 128)
    sizes = [1,2,3,4]
    ents = []
    for sz in sizes:
        e = entropy(data_ascii, sz)
        ents.append(e)
        print(f"Symbol size {sz} bytes: entropy = {e:.4f}")
    plt.plot(sizes, ents, marker='o')
    plt.xlabel('Symbol size (bytes)')
    plt.ylabel('Entropy (bits per symbol)')
    plt.title('Entropy vs symbol size')
    plt.show()

def test_mtf():
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    mtf_data = mtf_encode(data)
    e_orig = entropy(data, 1)
    e_mtf = entropy(mtf_data, 1)
    print(f"Original entropy: {e_orig:.4f}, MTF entropy: {e_mtf:.4f}")
    # проверка декодирования
    dec = mtf_decode(mtf_data)
    assert dec == data

def test_huffman():
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    bits, codes = huffman_encode(data)
    dec = huffman_decode(bits, codes)
    assert dec == data
    print(f"Huffman: {len(bits)/8} bytes, original: {len(data)} bytes, ratio: {len(bits)/8/len(data):.3f}")

def test_bwt():
    # маленький тест
    data = b"banana"
    bwt_data = bwt(data)
    inv = inverse_bwt(bwt_data)
    assert inv == data
    # с блоком
    data = b"abcdefghijklmnopqrstuvwxyz" * 100
    bwt_data = bwt(data, block_size=100)
    inv = inverse_bwt(bwt_data, block_size=100)
    assert inv == data
    print("BWT test passed")

def test_lz77():
    data = b"abracadabra"
    enc = lzss_encode(data, 4096, 18)
    dec = lzss_decode(enc)
    assert dec == data
    print("LZSS test passed")

def test_lzw():
    data = b"ababababababab"
    enc = lzw_encode(data, 256)
    dec = lzw_decode(enc, 256)
    assert dec == data
    print("LZW test passed")

# ------------------- Исследования -------------------
def bwt_entropy_vs_block():
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    block_sizes = [64, 128, 256, 512, 1024, 2048, 4096]
    orig_ent = entropy(data, 1)
    ents = []
    for bs in block_sizes:
        bwt_data = bwt(data, bs)
        e = entropy(bwt_data, 1)
        ents.append(e)
        print(f"Block size {bs}: entropy = {e:.4f}")
    plt.plot(block_sizes, ents, label='BWT entropy')
    plt.axhline(y=orig_ent, color='r', linestyle='--', label='Original entropy')
    plt.xlabel('Block size (bytes)')
    plt.ylabel('Entropy (bits per byte)')
    plt.title('BWT entropy vs block size')
    plt.legend()
    plt.show()

def lzss_ratio_vs_window():
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    window_sizes = [256, 512, 1024, 2048, 4096, 8192]
    ratios = []
    for ws in window_sizes:
        enc = lzss_encode(data, ws, 18)
        ratio = len(enc) / len(data)
        ratios.append(ratio)
        print(f"Window {ws}: ratio = {ratio:.3f}")
    plt.plot(window_sizes, ratios, marker='o')
    plt.xlabel('Window size (bytes)')
    plt.ylabel('Compression ratio')
    plt.title('LZSS compression ratio vs window size')
    plt.show()

def lzw_ratio_vs_dict():
    with open('test_data/enwik7', 'rb') as f:
        data = f.read()
    dict_sizes = [256, 512, 1024, 2048, 4096, 8192]
    ratios = []
    for ds in dict_sizes:
        enc = lzw_encode(data, ds)
        ratio = len(enc) / len(data)
        ratios.append(ratio)
        print(f"Dict size {ds}: ratio = {ratio:.3f}")
    plt.plot(dict_sizes, ratios, marker='o')
    plt.xlabel('Dictionary size (entries)')
    plt.ylabel('Compression ratio')
    plt.title('LZW compression ratio vs dictionary size')
    plt.show()

# ------------------- Сборка компрессоров -------------------
def all_compressors():
    results = {}
    for name, path in test_files.items():
        with open(path, 'rb') as f:
            data = f.read()
        original_size = len(data)
        # RLE
        enc = compress_rle(data)
        results[(name, 'RLE')] = len(enc) / original_size
        # BWT+RLE (блок 1024)
        enc = compress_bwt_rle(data, 1024)
        results[(name, 'BWT+RLE')] = len(enc) / original_size
        # BWT+MTF+HA (словарь нужно сохранять отдельно, для простоты опускаем)
        # LZSS (окно 4096)
        enc = compress_lzss(data)
        results[(name, 'LZSS')] = len(enc) / original_size
        # LZSS+HA
        enc = compress_lzss_huffman(data)
        results[(name, 'LZSS+HA')] = len(enc) / original_size
        # LZW (словарь 4096)
        enc = compress_lzw(data)
        results[(name, 'LZW')] = len(enc) / original_size
        # LZW+HA
        enc = compress_lzw_huffman(data)
        results[(name, 'LZW+HA')] = len(enc) / original_size
    # печать таблицы
    print("Compression ratios:")
    for (name, comp), ratio in results.items():
        print(f"{name:15} {comp:12}: {ratio:.4f}")

if __name__ == "__main__":
    test_rle()
    entropy_study()
    test_mtf()
    test_huffman()
    test_bwt()
    test_lz77()
    test_lzw()
    bwt_entropy_vs_block()
    lzss_ratio_vs_window()
    lzw_ratio_vs_dict()
    all_compressors()