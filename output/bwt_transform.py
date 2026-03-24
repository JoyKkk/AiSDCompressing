from bwt_transform import bwt_encode, bwt_decode_fast
import os

BLOCK_SIZE = 5000 # Small enough to be fast, large enough to group letters

def process_file_bwt(filename):
    path = f"data/{filename}"
    if not os.path.exists(path): return

    with open(path, "rb") as f:
        data = f.read()

    print(f"\nProcessing {filename} in blocks...")

    all_encoded = bytearray()
    indices = [] # We must save the index for every block!

    # 1. Encode in blocks
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i : i + BLOCK_SIZE]
        encoded_block, idx = bwt_encode(block)
        all_encoded.extend(encoded_block)
        indices.append(idx)

    # 2. how RLE likes this BWT data
    from rle_compressor import rle_encode
    rle_only = rle_encode(data)
    bwt_then_rle = rle_encode(all_encoded)

    print(f"Original Size: {len(data)} bytes")
    print(f"RLE Only Size: {len(rle_only)} bytes")
    print(f"BWT + RLE Size: {len(bwt_then_rle)} bytes")
    print(f"Improvement: {len(rle_only) / len(bwt_then_rle):.2f}x better")

if __name__ == "__main__":
    process_file_bwt("rus.txt")