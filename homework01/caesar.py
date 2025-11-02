"""
Caesar Cipher Implementation

"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    amount_of_letters = 26  # кол-во букв в английском алфавите
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                basechar = "A"
            else:
                basechar = "a"
            shifted_char = chr(
                ord(basechar)
                + ((ord(char) - ord(basechar) + shift) % amount_of_letters)
            )
            ciphertext += shifted_char

        else:
            ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    amount_of_letters = 26  # кол-во букв в английском алфавите
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                basechar = "A"
            else:
                basechar = "a"
            shifted_char = chr(
                ord(basechar)
                + ((ord(char) - ord(basechar) - shift) % amount_of_letters)
            )
            plaintext += shifted_char

        else:
            plaintext += char

    return plaintext
