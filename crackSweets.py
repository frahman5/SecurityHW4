def guessPassword(sweetwords):
    """
    listOfStrings -> string

    Given a list of sweetwords that we assume to contain 1 real password, 
    guesses and returns what that 1 real password is

    Runs the sweetwords through 4 rounds of "pruning," each round removes
    words we believe to be fakes under different subcases of the driving
    hypothesis: real passwords are based on real words. 
    """
    import random

    ## Round 1: If there are sweets with real words, get rid of sweets without real words
    guesses_1 = sweetwords
    subwords = {}
    for word in sweetwords:
        subword_tuple = getSubwords(word)
        if len(subword_tuple) == 0: # no subwords
            guesses_1.remove(word)
            continue
        subwords[word] = subword

    ## ROUND 2: Assume that sweets with more subwords than other sweets are better
    guesses_2 = shortestNonEmpty(sweetwords, guesses_1)
    assert len(guesses_2) == len(subwords.keys())
    max_num_words = max(len(list_of_subwords) for word, list_of_subwords in subwords)
    for word in sweetwords:
        if word not in guesses_2:
            continue
        num_subwords = len(subwords[word])
        if num_subwords < max_num_words:
            guesses_2.remove(word)
            del subwords[word]

    ## Round 3: Assume that sweets with longer subwords are better
    guesses_3 = shortestNonEmpty(sweetwords, guesses_1, guesses_2)
    assert len(guesses_3) == len(subwords.keys())
    max_length_word = getMaxLengthWord(subwords)
    for word in sweetwords:
        if word not in guesses_3:
            continue
        len_longest_subword = max((len(subword) for subword in word_info[word]))
        if len_longest_subword < max_length_word:
            guesses_3.remove(word)
            del subwords[word]

    ## Round 4: If reverse munging results in more subwords, its probably a password
    guesses_4 = shortestNonEmpty(sweetwords, guesses_1, guesses_2, guesses_3)
    assert len(guesses_4) == len(subwords.keys())
    for word in sweetwords:
        if word not in guesses_4:
            continue
        reverse_munged_sweet = reverseMunge(word)
        if len(getSubwords(reverse_munged_sweet)) <= len(word_info[word]):
            guesses_4.remove(word)

    ## Make a choice: Return a random choice from our pruned list
    final_guess_list = shortestNonEmpty(sweetwords, guesses_1, guesses_2, guesses_3, guesses_4)
    return random.choice(final_guess_list)

def getMaxLengthWord(subword):
    """
    dict -> int
    """
    tuples_of_lengths = ((len(subword) for subword in list_of_subwords) for 
                          word, list_of_subwords in subwords)
    all_lengths = (length in tuple_of_lens for tuple_of_lens in tuples_of_lengths)
    max_length_word = max(all_lengths)

    return max_length_word

def getSubwords(word):
    """
    string -> listOfStrings

    Given a string, returns a list of all english language words that are 
    contained in the string
    """
    pass

def reverseMunge(sweetword):
    """
    string -> string

    Given a string, "reverse munges" nonalpha characters to "close" alpha characters
    (e.g 5->s) and returns the resultant string
    """
    pass

def shortestNonEmpty(*args):
    """
    list list ... list -> list

    Given greater than or equal to 1 lists, returns a copy the shortest non-length-zero
    list. Raises an error if all lists are of length 0
    """
    if len(*args) == 0:
        raise ValueError("Must input at least 1 list to shortestNonEmpty")

    lengths = [len(input_list) for input_list in *args]
    if sum(lengths) == 0:
        raise ValueError("At least one input list to shortestNonEmpty must have nonzero length")

    return [elem for elem in *args[lengths.index(min(lengths))]]

if __name__ == '__main__':
    ## 1 test for getSubwords

    ## 1 test for shortestNonEmpty

    ## 1 test for reverseMunge
    pass
