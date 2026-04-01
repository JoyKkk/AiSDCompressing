def bwt_encode(data):
    if not data:
        return b'', 0
    n = len(data)
    rotations = [(data[i:] + data[:i], i) for i in range(n)]
    rotations.sort(key = lambda x: x[0])
    last_col = bytearray([r[0][-1] for r in rotations])
    primary_idx = 0
    for i, (rot, idx) in enumerate(rotations):
        if idx == 0:
            primary_idx = i
            break
    return bytes(last_col), primary_idx

def bwt_decode(data, primary_idx):
    if not data:
        return b''
    n = len(data)
    counts = {}
    ranks = []
    for byte in data:
        rank = counts.get(byte, 0)
        ranks.append(rank)
        counts[byte] = rank + 1
    first_col = sorted(data)
    char_starts = {}
    for i, byte in enumerate(first_col):
        if byte not in char_starts:
            char_starts[byte] = i
    
    decoded = bytearray(n)
    curr = primary_idx

    for i in range(n - 1, -1, -1):
        decoded[i] = data[curr]
        curr = char_starts[data[curr]] + ranks[curr]
    return bytes(decoded)

if __name__ == "__main__":
    test = b"banana"
    enc, idx = bwt_encode(test)
    dec = bwt_decode(enc, idx)
    print(enc, idx)
    print("Совпадает? -", test == dec)