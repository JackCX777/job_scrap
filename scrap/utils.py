cyrillic_letters = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ь': '',
    'ъ': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya'
}


def from_cyrillic_to_latin(text: str):
    text = text.replace(' ', '_').lower()
    tmp = ''
    for symbol in text:
        tmp += cyrillic_letters.get(symbol, symbol)  # if symbol doesn't exist in cyrillic_letters dict, default symbol.
    return tmp
