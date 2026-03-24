import os

def rle_encode(data, Ms=8):
    s_bytes = Ms // 8
    encoded = bytearray()
    i = 0
    while i < len(data):
        run_length = 1
        current_symbol = data[i : i + s_bytes]
        while i + (run_length * s_bytes) < len(data):
            if data[i + (run_length * s_bytes) : i + (run_length + 1) * s_bytes] == current_symbol and run_length < 127:
                run_length += 1
            else:
                break
        if run_length > 1:
            encoded.append(run_length)
            encoded.extend(current_symbol)
            i += run_length * s_bytes
        else:
            unique_seq = []
            while i < len(data):
                if i + (2 * s_bytes) <= len(data):
                    if data[i : i + s_bytes] == data[i + s_bytes : i + 2 * s_bytes]:
                        break
                unique_seq.extend(data[i : i + s_bytes])
                i += s_bytes
                if len(unique_seq) // s_bytes >= 127:
                    break
            count = len(unique_seq) // s_bytes
            encoded.append(count | 0x80)
            encoded.extend(unique_seq)
    return encoded

def run_full_test(filename, Ms_bits):
    path = f"data/{filename}"
    if not os.path.exists(path):
        print(f"File {filename} missing!")
        return
    with open(path, "rb") as f:
        data = f.read()

    compressed = rle_encode(data, Ms=Ms_bits)
    ratio = len(data) / len(compressed)
    print(f"{filename.ljust(11)} | Оригинал: {len(data):>10} | Сжатая вер. {len(compressed):>10} | Коэф.: {ratio:.2f}")

if __name__ == "__main__":
    print("\n" + "="*76)
    print("    Файл    |    Исходный размер   |     Сжатый размер      | Коэф. сжатия")
    print("-" * 76)
    run_full_test("rus.txt", 8)
    run_full_test("binary.exe", 8)
    run_full_test("enwik7.txt", 8)
    run_full_test("bw.raw", 8)
    run_full_test("gray.raw", 8)
    run_full_test("color.raw", 24) # Ms=24 for Color
    print("="*76 + "\n")