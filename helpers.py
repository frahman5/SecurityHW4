import string
import bz2
import zipfile

replacements = {
    'a': {'a','A','@','4'},
    'b': {'b','B','8','6'},
    'c': {'c','C','('},
    'd': {'d','D',')','?','6'},
    'e': {'e','E','3','&'},
    'f': {'f','F','6','9','&','#'},
    'g': {'g','G','9'},
    'h': {'h','H','#'},
    'i': {'i','I','!','1','|'},
    'j': {'j','J',']'},
    'k': {'k','K','X','<'},
    'l': {'l','L','|','1','7'},
    'm': {'m','M'},
    'n': {'n','N'},
    'o': {'o','O','0'},
    'p': {'p','P','9'},
    'q': {'q','Q','9'},
    'r': {'r','R','2'},
    's': {'s','S','5','$','z'},
    't': {'t','T','7','+'},
    'u': {'u','U','v'},
    'v': {'v','V','^'},
    'w': {'w','W'},
    'x': {'x','X','%','*'},
    'y': {'y','Y','J','j','?'},
    'z': {'z','Z','2','%'},
    '1': {'1','7','i','I','l','!','|'},
    '2': {'2','z','Z'},
    '3': {'3','E'},
    '4': {'4','A','h'},
    '5': {'5','s','$'},
    '6': {'6','b'},
    '7': {'7','1','L'},
    '8': {'8','6','B'},
    '9': {'9','p','P','q'},
    '0': {'0','o','O'},
    '@': {'a','A','@','4'},
    '(': {'c','C','('},
    ')': {'d','D',')','?','6'},
    '?': {'a','A','@','4'},
    '&': {'e','E','3','&','f','F','6','9','#'},
    '#': {'e','E','3','&','f','F','6','9','#','h','H','#'},
    '!': {'1','7','i','I','l','!','|'},
    '|': {'1','7','i','I','l','!','|'},
    ']': {'j','J',']'},
    '<': {'k','K','X','<'},
    '$': {'s','S','5','$','z'},
    '+': {'t','T','7','+'},
    '^': {'v','V','^'},
    '%': {'x','X','%','*','z','Z','2','%'},
    '*': {'x','X','%','*'},
}

def unMunge(char):
    """
    :param char: character
    :return: :
    """
    return replacements[char].intersection(set(string.ascii_lowercase))

def isWord(stringOfLetters):
    """
    string -> bool

    Returns True if stringOfLetters is in the english dictionary,
    false otherwise
    """
    import enchant              ## PyEnchant library allows dictionary lookups
    englishDict = enchant.Dict("en_US")
    return englishDict.check(stringOfLetters)