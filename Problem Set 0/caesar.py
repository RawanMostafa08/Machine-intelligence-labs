from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''

def shift_string(shift: int,word:str)->str:
    shifted = []
    
    for char in word:
        new_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
        shifted.append(new_char)

    return ''.join(shifted)

DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    words=ciphered.split(" ")
    min_missing = float('inf')
    best_res=""
    best_shift=0
    dict_set = set(dictionary)

    for shift in range(26):
        deciphered_words = []
        missing = 0
        for word in words:
            deciphered_word=shift_string(shift,word)
            deciphered_words.append(deciphered_word)
            if deciphered_word not in dict_set:
                missing+=1
        if missing < min_missing:
            min_missing=missing
            best_shift=shift
            best_res = ' '.join(deciphered_words)
        if min_missing == 0:
            break
    return (best_res,best_shift,min_missing)



