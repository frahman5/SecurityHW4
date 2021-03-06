import helpers
import string

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
    guesses_1 = shortestNonEmpty(sweetwords)
    subwords_dict = {}
    for word in sweetwords:
        subword_tuple = getSubwords(word)
        # print "word: {} subword_tuple: {} ".format(word, subword_tuple)
        if len(subword_tuple) == 0: # no subwords
            guesses_1.remove(word)
            continue
        subwords_dict[word] = subword_tuple

    if len(guesses_1) != 0:
        ## ROUND 2: Assume that sweets with more subwords than other sweets are better
        guesses_2 = shortestNonEmpty(sweetwords, guesses_1)
        max_num_words = max(len(list_of_subwords) for list_of_subwords in subwords_dict.itervalues())
        for word in sweetwords:
            if word not in guesses_2:
                continue
            num_subwords = len(subwords_dict[word])
            if num_subwords < max_num_words:
                guesses_2.remove(word)
                del subwords_dict[word]

        ## Round 3: Assume that sweets with longer subwords are better
        guesses_3 = shortestNonEmpty(sweetwords, guesses_1, guesses_2)
        max_length_word = getMaxLengthWord(subwords_dict)
        for word in sweetwords:
            if word not in guesses_3:
                continue
            len_longest_subword = max((len(subword) for subword in subwords_dict[word]))
            if len_longest_subword < max_length_word:
                guesses_3.remove(word)
                del subwords_dict[word]
    else:
        guesses_2 = []
        guesses_3 = []

    ## Round 4: If reverse munging results in more subwords, its probably a password
    guesses_4 = shortestNonEmpty(sweetwords, guesses_1, guesses_2, guesses_3)
    for word in sweetwords:
        # skip the unnecessary ones
        if word not in guesses_4:
            continue

        # reverse munge it to find more words
        reverse_munged_sweet = reverseMunge(word)

        # how many subwords did we used to have?
        num_previous_words = 0
        if len(guesses_1) != 0:
            num_previous_words = len(subwords_dict[word])

        # if we dont have more now, remove it
        if len(getSubwords(reverse_munged_sweet)) <= num_previous_words:
            guesses_4.remove(word)

    ## Make a choice: Return a random choice from our pruned list
    final_guess_list = shortestNonEmpty(sweetwords, guesses_1, guesses_2, guesses_3, guesses_4)
    return random.choice(final_guess_list)

def getMaxLengthWord(subword_dict):
    """
    dict -> int

    dict format is 
        word: (subword1, subword2, ..., subwordn)
    """
    ## Construct a list of the lengths of all the subwords in subword_dict values
    all_lengths = []
    for key in subword_dict.keys():
        for subword in subword_dict[key]:
            all_lengths.append(len(subword))

    ## Return the max
    max_length_word = max(all_lengths)

    return max_length_word

def getSubwords(word):
    """
    string -> listOfStrings

    Given a string, returns a list of all english language words that are 
    contained in the string
    """
    subwordArray = []

    #start from the index of the last letter, and go back,
    for i in xrange(0,len(word)):
        #start from the first letter, up to the letter we're checking.
        for j in xrange(len(word), 0, -1):
            if j - i > 1:
                subword = word[i:j]
                # print "considering word: {}".format(word[i:j])
                if helpers.isWord(subword):
                    subwordArray.append(word[i:j])
                    break
                else:
                    continue

    # Remove subwords of subwords (e.g if we have 'bicycle' and 'cycle', we only
    # want 'bicycle')
    subwordArrayCopy1 = [elem for elem in subwordArray]
    subwordArrayCopy2 = [elem for elem in subwordArray]
    for word1 in subwordArrayCopy1:
        for word2 in subwordArrayCopy2:
            if word2 == word1:
                continue
            if word1 in word2:
                subwordArray.remove(word1)
                break

    return subwordArray

def reverseMunge(sweetword):
    """
    string -> string

    Given a string, "reverse munges" nonalpha characters to "close" alpha characters
    (e.g 5->s) and returns the resultant string
    """
    cleanword = ''
    for char in sweetword:
        cleanword += helpers.unMunge(char)

    return cleanword


def shortestNonEmpty(*args):
    """
    list list ... list -> list

    Given greater than or equal to 1 lists, returns a copy the shortest non-length-zero
    list. Raises an error if all lists are of length 0
    """
    ## Make sure we got at least one list as input
    if len(args) == 0:
        raise ValueError("Must input at least 1 list to shortestNonEmpty")

    ## Calculate the lengths of all the lists, and replace zeros with infinity
    lengths = [len(input_list) for input_list in args]
    if sum(lengths) == 0:
        raise ValueError("At least one input list to shortestNonEmpty must have nonzero length")
    lengths = [length if length != 0 else float('inf') for length in lengths]

    ## Return a copy of the shortest non empty list
    return [elem for elem in args[lengths.index(min(lengths))]]

if __name__ == '__main__':
    ## 1 test for getMaxLength Words
    test_subword_dict = {
                          'bicycle76alpha': ('bicycle', 'alpha'),
                          '#spongebob': ('sponge', 'bob')
                        }
    assert (getMaxLengthWord(test_subword_dict) == 7)

    ## 1 test for shortestNonEmpty
    test_list_1 = ['heyyo', 'mypassword', 'here', 'stupidpassword', 'jessica']
    test_list_2 = []
    test_list_3 = ['heyyo', 'here']
    assert (shortestNonEmpty(test_list_1, test_list_2, test_list_3) == test_list_3)

    ## 1 test for reverseMunge
    test_password = '#5pongEbobmyM@ns0d0ntt0uchh!m'
    assert (reverseMunge(test_password) == 'hspongebobmymansodonttouchhim')

    ## 1 test for getSubwords
    test_password_1 = 'bicycle76alpha'
    test_password_2 = '#spongebob'
    assert set(getSubwords(test_password_1)) == set(test_subword_dict[test_password_1])
    assert set(getSubwords(test_password_2)) == set(test_subword_dict[test_password_2])
    print "all tests passed!"

    ## test for guessPasswords
    import os
    # pathtest = '/Users/faiyamrahman/Documents/CTech/SecurityAndPrivacyConcepts/HW4/test'
    path1 = 'tocrack/Group FROZA'
    path2 = 'tocrack/group1'
    path3 = 'tocrack/group3_pswds'
    path4 = 'tocrack/honeywords'
    path5 = 'tocrack/TeamShaZafDan'
    for path in (path3, path4, path5):
        guesses = []
        files = os.listdir(path)
        if '.DS_Store' in files:
            files.remove('.DS_Store')
        files.sort(key=lambda filename: int(filename))
        for filename in files:
            print filename
            if filename == '2':
                import pdb
                pdb.set_trace()
            # open it
            with open(path + '/' + filename, 'r') as f:
                # get the sweets
                sweets = f.readlines()
                sweets = [sweet.replace('\n','').replace('\r','') for sweet in sweets]
                
                # guess the passwords
                guesses.append(guessPassword(sweets) + '\n')

        group_name = path.split('/')[-1] + '_cracked.csv'
        with open(group_name, "w+") as output_file:
            output_file.writelines(guesses)
        # print guess_dict
    
    
