def encrypt_caesar(plaintext, shift=3):
    ciphertext = ""
    for c in plaintext:
        n = 0
        if ord("A") <= ord(c) <= ord("Z"):
            ciphertext += chr(((ord(c) - ord("A") + shift) % 26) + ord("A"))
        elif ord("a") <= ord(c) <= ord("z"):
            ciphertext += chr(((ord(c) - ord("a") + shift) % 26) + ord("a"))
        else:
            ciphertext += c
    return ciphertext


def decrypt_caesar(ciphertext, shift=3):
    plaintext = ""
    for c in ciphertext:
        n = 0
        if ord("A") <= ord(c) <= ord("Z"):
            plaintext += chr(((ord(c) - ord("A") - shift) % 26) + ord("A"))
        elif ord("a") <= ord(c) <= ord("z"):
            plaintext += chr(((ord(c) - ord("a") - shift) % 26) + ord("a"))
        else:
            plaintext += c
    return plaintext
