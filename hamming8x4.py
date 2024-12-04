def encode_byte(byte):
    d1 = (byte >> 3) & 1
    d2 = (byte >> 2) & 1
    d3 = (byte >> 1) & 1
    d4 = (byte >> 0) & 1

    p1 = 1 ^ d1 ^ d3 ^ d4
    p2 = 1 ^ d1 ^ d2 ^ d4
    p3 = 1 ^ d1 ^ d2 ^ d3
    p4 = 1 ^ p1 ^ p2 ^ p3 ^ d1 ^ d2 ^ d3 ^ d4

    result = 0
    result |= (p1 << 7)
    result |= (d1 << 6)
    result |= (p2 << 5)
    result |= (d2 << 4)
    result |= (p3 << 3)
    result |= (d3 << 2)
    result |= (p4 << 1)
    result |= (d4 << 0)

    return result


def encode(data):
    print("Encoding...")
    result = []
    for byte in data:
        encoded_byte = encode_byte(byte)
        print(f"{bin(byte)[2:].zfill(4)} -> {bin(encoded_byte)[2:].zfill(8)}")
        result.append(encoded_byte)
    return result


def decode_byte(byte, index):
    p1 = (byte & 0b10000000) != 0
    p2 = (byte & 0b00100000) != 0
    p3 = (byte & 0b00001000) != 0
    p4 = (byte & 0b00000010) != 0
    d1 = (byte & 0b01000000) != 0
    d2 = (byte & 0b00010000) != 0
    d3 = (byte & 0b00000100) != 0
    d4 = (byte & 0b00000001) != 0

    A = p1 ^ d1 ^ d3 ^ d4 == 1
    B = p2 ^ d1 ^ d2 ^ d4 == 1
    C = p3 ^ d1 ^ d2 ^ d3 == 1
    D = p1 ^ p2 ^ p3 ^ p4 ^ d1 ^ d2 ^ d3 ^ d4 == 1

    if (not A or not B or not C) and D:
        return None  # Double error

    error_pos = int(not A) + int(not B) * 2 + int(not C) * 4 + int(not D) * 8

    if error_pos > 0:
        print(f"In byte {index}, an error was corrected in the {error_pos}-th bit.")
        if error_pos == 15:
            d1 ^= 1
        elif error_pos == 14:
            d2 ^= 1
        elif error_pos == 13:
            d3 ^= 1
        elif error_pos == 11:
            d4 ^= 1

    return (d1 << 3) | (d2 << 2) | (d3 << 1) | d4


def decode(data):
    print("Decoding...")
    result = []
    for index, byte in enumerate(data, start=1):
        decoded_byte = decode_byte(byte, index)
        if decoded_byte is None:
            print(f"{index}. {bin(byte)[2:].zfill(8)} -> Double error.")
            return None
        print(f"{index}. {bin(byte)[2:].zfill(8)} -> {bin(decoded_byte)[2:].zfill(4)}")
        result.append(decoded_byte)
    return result

def split_into_blocks(number):
    binary = bin(number)[2:]
    while len(binary) % 4 != 0:
        binary = "0" + binary

    print(f"Number {number} in binary representation: {binary}")

    result = []
    for i in range(0, len(binary), 4):
        block = binary[i:i + 4]
        result.append(int(block, 2))
        print(f"{block}")
    return result


def invert_bit(data, block_index, bit_index):
    if 1 <= bit_index <= 8:
        data[block_index] ^= (1 << (8 - bit_index))
        return data
    else:
        print("Error: bit index must be between 1 and 8.")
        return data
