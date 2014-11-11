import string
import bz2
import zipfile

replacements = {
    '1': {'1','7','i','I','!','|'},
    '2': {'2','z','Z'},
    '3': {'3','E','e'},
    '4': {'4','A','a'},
    '5': {'5','s','$'},
    '6': {'6','b'},
    '7': {'7','1','l'},
    '8': {'8','6','b'},
    '9': {'9','p','P'},
    '0': {'0','o','O'},
    '@': {'a','A','@','4'},
    '(': {'c','C','('},
    ')': {'d','D',')','?','6'},
    '?': {'a','A','@','4'},
    '&': {'e','E','3','&','6','9','#'},
    '#': {'3','&','6','9','#','h','H','#'},
    '!': {'1','7','i','I','!','|'},
    '|': {'1','7','i','I','!','|'},
    ']': {'j','J',']'},
    '/': {'l'},
    ':': {'l'},
    '<': {'x','<'},
    '$': {'s','S','5','$'},
    '+': {'t','T','7','+'},
    '^': {'v','V','^'},
    '%': {'x','X','%','*','2','%'},
    '*': {'x','X','%','*'},
}

def unMunge(char):
    """
    :param char: character
    :return: :
    """
    retval = None

    # if its a normal character, return it
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    others = ' _.,;-'
    if char in characters:
        retval = char.lower()
    elif char in others:
        retval = char
    else:
        try:
            retval = replacements[char].intersection(set(string.ascii_lowercase)).pop()
        except:
            print "add {} to others in unMunge.".format(char)
            retval = char

    return retval

def isWord(stringOfLetters):
    """
    string -> bool

    Returns True if stringOfLetters is in the english dictionary,
    false otherwise
    """
    import enchant              ## PyEnchant library allows dictionary lookups
    englishDict = enchant.Dict("en_US")
    return englishDict.check(stringOfLetters)