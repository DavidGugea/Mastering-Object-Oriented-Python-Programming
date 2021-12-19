def caesar(text: str, key: int) -> str:
    result: str = ""
    for char in text:
        c: int = ord(char)
        end_char: str = chr(c + key)
        result += end_char

    return result


print(caesar("vguvauvtkpi", -2))
