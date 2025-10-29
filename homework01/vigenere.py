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
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                shift = ord(keyword[keyidx % len(keyword)]) - ord('A')
                shifted_char = chr(ord('A') + ((ord(char) - ord('A') + shift) % 26))
                ciphertext += shifted_char
            else:
                shift = ord(keyword[keyidx % len(keyword)]) - ord('a')
                shifted_char = chr(ord('a') + ((ord(char) - ord('a') + shift) % 26))
                ciphertext += shifted_char

        else:
            ciphertext += char
        keyidx += 1
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
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                shift = ord(keyword[keyidx % len(keyword)]) - ord('A')
                shifted_char = chr(ord('A') + ((ord(char) - ord("A") - shift) % 26))
                plaintext += shifted_char
            else:
                shift = ord(keyword[keyidx % len(keyword)]) - ord('a')
                shifted_char = chr(ord('a') + ((ord(char) - ord('a') - shift) % 26))
                plaintext += shifted_char
        else:
            plaintext += char
        keyidx += 1
    return plaintext
