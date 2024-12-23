def encrypt_string(data: str, key: str) -> str:
    if data == None or key == None:
        return None
    
    output = [ord(char) ^ ord(key[i % len(key)]) for i, char in enumerate(data)]
    output = bytes(output).hex()
    return output


def decrypt_string(data: bytes, key: str) -> str:
    if data == None or key == None:
        return None
    
    new_data = bytes.fromhex(data)
    output = "".join([chr(nbr ^ ord(key[i % len(key)])) for i, nbr in enumerate(new_data)])
    return output