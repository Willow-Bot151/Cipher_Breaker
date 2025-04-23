from pprint import pprint
import math

class EncryptedStrings():
    def __init__(self, list_of_strings: str = None):
        self.strings_to_encrypt = list_of_strings
    def caeser_shift_char(self, character, shift):
        char_code = self.get_char_code(character)
        char_case = self.is_char_letter_and_what_case(char_code)
        if char_case:
            char_code += shift
            if self.is_char_letter_and_what_case(char_code) != char_case:
                char_code -= 26
        encrypted_char = char_code.to_bytes().decode('utf-8')
        return encrypted_char
    def get_char_code(self,char):
        char_code = int.from_bytes(char.encode('utf-8'),byteorder='little')
        return char_code
    def is_char_letter_and_what_case(self,char_code):
        if char_code < 65:
            return False
        elif char_code < 91:
            return 'lower'
        elif char_code < 97:
            return False
        elif char_code < 123:
            return 'upper'
        else:
            return False
    def caeser_shift_string(self, string, shift):
        new_string = ''
        for i in range(len(string)):
            new_string += self.caeser_shift_char(string[i], shift)
        return new_string
    def Vigenere_cipher_encrypt_string(self,string,key):
        encrypted_string = ""
        position = 0
        key_lenth = len(key)
        for char_pos in range(len(string)):
            if self.is_char_letter_and_what_case(self.get_char_code(string[char_pos])):
                shift = self.get_char_code(key[position % key_lenth]) - 97
                position += 1
            encrypted_char = self.caeser_shift_char(
                character=string[char_pos],
                shift=shift)
            encrypted_string += encrypted_char
        return encrypted_string

class CipherBreaker():
    def __init__(self,encrypted_string : str = None):
        string = encrypted_string
        english_words = None
    def decrypt_string(self):
        pass
    def order_by_amount_of_common_words(self, list_of_strings):
        new_list = list_of_strings
        new_list.sort(reverse=True,key=self.find_proportion_of_common_words_in_a_string)
        return new_list
    def find_proportion_of_common_words_in_a_string(self, string):
        with open('data/common_word_list','r') as f:
            self.english_words = f.read()
        list_of_english_words = self.english_words.split("\n")
        words = string.split(" ")
        # assuming clean
        no_of_words = len(words)
        no_of_common_words = 0
        for word in words:
            if word.lower() in list_of_english_words:
                no_of_common_words += 1
        return no_of_common_words / no_of_words
    def caeser_shift_decrypt(self,some_string:str):
        possibility_list = []
        for shift in range(26):
            shifted_string = ""
            for char in range(len(some_string)):
                shifted_char = self.caeser_shift_char(some_string[char],shift)
                shifted_string += shifted_char
            possibility_list.append(shifted_string)
        return possibility_list
    def caeser_shift_char(self, character, shift):
        utf_char = int.from_bytes(
            character.encode('utf-8'),
            byteorder='little')
        if utf_char > 96 and utf_char < 123:
            utf_char += shift
            if utf_char > 122:
                utf_char -= 26
        elif utf_char > 64 and utf_char < 91:
            utf_char += shift
            if utf_char > 90:
                utf_char -= 26
        encrypted_char = utf_char.to_bytes().decode('utf-8')
        return encrypted_char
    def vigenere_cipher_decrypt_kasiski_test(self, string):
        stripped_string = self.strip_whitespace(string)
    def strip_whitespace(self,string):
        new_string = string.replace(" ","").replace("\n","").replace("\t","")
        return new_string
    def find_all_substrings(self, string):
        stripped_string = self.strip_whitespace(string)
        length = len(stripped_string)
        substrings = []
        for start in range(length):
            for end in range(start+2,length+1):
                substrings.append(stripped_string[start:end])
        return substrings
    def find_repeats_of_substrings(self, string):
        stripped_string = self.strip_whitespace(string)
        substrings = self.find_all_substrings(stripped_string)
        occurances_of_substrings = dict()

        for substring in substrings:
            if len(substring) < 3:
                continue
            num_of_occurances = self.count_occurances_of_substring(substring,stripped_string)
            if num_of_occurances < 2:
                continue

            occurances_of_substrings[substring] ={
                    'repeats' : num_of_occurances,
                    'distances' : self.calculate_distances_between_substrings(
                        self.record_position_of_repeated_substrings(
                            substring=substring,
                            string=stripped_string
                        )
                    )
                }
        pprint(occurances_of_substrings)
        return occurances_of_substrings
    def record_position_of_repeated_substrings(self,substring,string):
        substring_length = len(substring)
        positions = []
        for i in range(len(string)):
            if string[i:i+substring_length] == substring:
                positions.append((i,i+substring_length))
        return positions
    def count_occurances_of_substring(self,substring, string):
        substring_length = len(substring)
        count = 0
        for i in range(len(string)):
            if string[i:i+substring_length] == substring:
                count += 1
        return count
    def calculate_distances_between_substrings(self, positions):
        distances = []
        occurances = len(positions)
        if occurances > 1:
            for i in range(1,occurances):
                for j in range(i):
                    distance = positions[i][0] - positions[j][0]
                    distances.append(distance)
        distances.sort()
        return distances
    def find_factors_up_to_limit_of_an_integer(self, number : int, limit : int = None):
        if limit == None:
            limit = number
        factors = []
        for i in range(int(math.sqrt(number))):
            possible_factor = i+1
            pair_factor = int(number/possible_factor)
            if number % possible_factor == 0:
                if possible_factor <= limit:
                    factors.append(possible_factor)
                if pair_factor <= limit:
                    factors.append(pair_factor)
        factors.sort()
        return factors
    def decide_key_length(self,substring_occurances : dict):
        """
        largest factor that appears most often
        most common of
            largest common denominator of distances between repeats

        best choice:
            most common factor
            large factor
            long substring
        
        number of repeats?

        input:
            'faf' : {
                'repeats' : 2,
                'distances' : [13]
            },
            'toe' : {
                'repeats' : 2,
                'distances' : [9]
            }
        
        factorise_func:
            takes: integer, k
            returns: list of factors, [a,b,c]
        
        for substring:
            factorise distances
            bucket of factors?

        for a key length possibility, k 
        weight(k) = n(k)
        """
        # factor_bucket = dict()
        # for k, v in substring_occurances.items():
        #     try:
        #         factor_bucket[f'{len(k)}-graph']
        #     except KeyError:
        #         factor_bucket[f'{len(k)}-graph'] = dict()
        #     for distance in v['distances']:
        #         factors = self.find_factors_up_to_limit_of_an_integer(distance)
        #         for factor in factors:
        #             try:
        #                 factor_bucket[f'{len(k)}-graph'][factor] += 1
        #             except KeyError as e:
        #                 factor_bucket[f'{len(k)}-graph'][factor] = 1
        # # for n_graph in factor_bucket.keys():
        # pprint(factor_bucket)
        factor_bucket = dict()
        for k, v in substring_occurances.items():
            for distance in v['distances']:
                factors = self.find_factors_up_to_limit_of_an_integer(distance)
                for factor in factors:
                    try:
                        factor_bucket[factor] += 1
                    except KeyError:
                        factor_bucket[factor] = 1
        max_occurances_of_factor = 0
        for k,v in factor_bucket.items():
            if v > max_occurances_of_factor:
                max_occurances_of_factor = v
        key_lengths = []
        for k,v in factor_bucket.items():
            if v == max_occurances_of_factor:
                key_lengths.append(k)
        pprint(factor_bucket)
        return max(key_lengths)
    def frequency_analysis(self, string):
        english_letter_frequencies = {
        'A' : 7.57,
        'B' : 1.84,
        'C' : 4.09,
        'D' : 3.38,
        'E' : 11.51,
        'F' : 1.23,
        'G' : 2.70,
        'H' : 2.32,
        'I' : 9.01,
        'J' : 0.16,
        'K' : 0.85,
        'L' : 5.31,
        'M' : 2.84,
        'N' : 6.85,
        'O' : 6.59,
        'P' : 2.94,
        'Q' : 0.16,
        'R' : 7.07,
        'S' : 9.52,
        'T' : 6.68,
        'U' : 3.27,
        'V' : 0.98,
        'W' : 0.74,
        'X' : 0.29,
        'Y' : 1.63,
        'Z' : 0.47}
        clean_string = self.strip_whitespace(string).upper()
        cipher_letter_frequencies = dict()
        length = len(clean_string)
        for k in english_letter_frequencies.keys():
            cipher_letter_frequencies[k] = (clean_string.count(k) * 100) / length
        pprint(cipher_letter_frequencies)