def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    for i in range(0, len(plaintext)):
        current_letter = ord(plaintext[i])
        if len(keyword) <= i:
            sdvig = ord(keyword[i - len(keyword) * (i // len(keyword))])
            if ord("A") <= sdvig <= ord("Z"):
                sdvig = sdvig - ord("A")
            elif ord("a") <= sdvig <= ord("z"):
                sdvig = sdvig - ord("a")
        else:
            sdvig = ord(keyword[i])
            if ord("A") <= sdvig <= ord("Z"):
                sdvig = sdvig - ord("A")
            elif ord("a") <= sdvig <= ord("z"):
                sdvig = sdvig - ord("a")
        if ord("A") <= current_letter <= ord("Z"):
            ciphertext += chr(((current_letter - ord("A") + sdvig) % 26) + ord("A"))
        elif ord("a") <= current_letter <= ord("z"):
            ciphertext += chr(((current_letter - ord("a") + sdvig) % 26) + ord("a"))
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    for i in range(0, len(ciphertext)):
        current_letter = ord(ciphertext[i])
        if len(keyword) <= i:
            sdvig = ord(keyword[i - len(keyword) * (i // len(keyword))])
            if ord("A") <= sdvig <= ord("Z"):
                sdvig = sdvig - ord("A")
            elif ord("a") <= sdvig <= ord("z"):
                sdvig = sdvig - ord("a")
        else:
            sdvig = ord(keyword[i])
            if ord("A") <= sdvig <= ord("Z"):
                sdvig = sdvig - ord("A")
            elif ord("a") <= sdvig <= ord("z"):
                sdvig = sdvig - ord("a")
        if ord("A") <= current_letter <= ord("Z"):
            plaintext += chr(((current_letter - ord("A") - sdvig) % 26) + ord("A"))
        elif ord("a") <= current_letter <= ord("z"):
            plaintext += chr(((current_letter - ord("a") - sdvig) % 26) + ord("a"))
        else:
            plaintext += ciphertext[i]
    return plaintext
