from hamming8x4 import encode, decode

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


def main():
    number = int(input("Enter an integer N that does not exceed 2^64-1: "))
    blocks = split_into_blocks(number)
    encoded_blocks = []
    decoded_blocks = []

    while True:
        print("\nCommand list:")
        print("1. Encode")
        print("2. Decode")
        print("3. Invert bit")
        print("4. Enter a new value")
        print("5. Exit")
        command = int(input("Select a command: "))

        if command == 1:
            encoded_blocks = encode(blocks)
            print("Encoded blocks:", [bin(block)[2:].zfill(8) for block in encoded_blocks])
        elif command == 2:
            if encoded_blocks:
                decoded_blocks = decode(encoded_blocks)
                if decoded_blocks:
                    print("Decoded binary result:", ''.join(bin(block)[2:].zfill(4) for block in decoded_blocks))
                else:
                    print("Data cannot be corrected.")
            else:
                print("Error: Encode data first.")
        elif command == 3:
            if encoded_blocks:
                block_index = int(input(f"Select block index (1-{len(encoded_blocks)}): ")) - 1
                bit_index = int(input("Select bit index (1-8): "))
                encoded_blocks = invert_bit(encoded_blocks, block_index, bit_index)
                print("Modified blocks:", [bin(block)[2:].zfill(8) for block in encoded_blocks])
            else:
                print("Error: Encode data first.")
        elif command == 4:
            number = int(input("Enter an integer N that does not exceed 2^64-1: "))
            blocks = split_into_blocks(number)
            encoded_blocks = []
        elif command == 5:
            print("Exiting...")
            break
        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()
