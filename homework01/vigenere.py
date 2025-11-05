def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyidx = 0
    amount_of_letters = 26

    for char in plaintext:
        if char.isalpha():
            base = "A" if char.isupper() else "a"
            shift = ord(keyword[keyidx % len(keyword)]) - ord(base)
            ciphertext += chr(ord(base) + ((ord(char) - ord(base) + shift) % amount_of_letters))
            keyidx += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyidx = 0
    amount_of_letters = 26

    for char in ciphertext:
        if char.isalpha():
            base = "A" if char.isupper() else "a"
            shift = ord(keyword[keyidx % len(keyword)]) - ord(base)
            plaintext += chr(ord(base) + ((ord(char) - ord(base) - shift) % amount_of_letters))
            keyidx += 1
        else:
            plaintext += char
    return plaintext