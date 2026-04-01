from bwt import bwt_encode, bwt_decode
import os

BLOCK_SIZE = 5000

def process_file_bwt(filename):
    path = f"data/{filename}"
    if not os.path.exists(path): return

    with open(path, "rb") as f:
        data = f.read()

    all_encoded = bytearray()
    indices = []

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i : i + BLOCK_SIZE]
        encoded_block, idx = bwt_encode(block)
        all_encoded.extend(encoded_block)
        indices.append(idx)

    from rle_compressor import rle_encode
    rle_only = rle_encode(data)
    bwt_then_rle = rle_encode(all_encoded)

    print(f"Исходный размер: {len(data)} байт")
    print(f"Размер после RLE: {len(rle_only)} байт")
    print(f"Размер после BWT + RLE: {len(bwt_then_rle)} байт")

if __name__ == "__main__":
    process_file_bwt("rus.txt")