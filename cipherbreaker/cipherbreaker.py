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
        for char_pos in range(len(string)):
            print('char_pos: ',char_pos)
            print('key_char: ',key[char_pos])
            if self.is_char_letter_and_what_case(self.get_char_code(string[char_pos])):
                shift = self.get_char_code(key[position]) - 97
                position += 1
            print('shift: ',shift)
            encrypted_char = self.caeser_shift_char(
                character=string[char_pos],
                shift=shift)
            print('encrypted_char: ',encrypted_char)
            encrypted_string += encrypted_char
        print('encrypted_string: ',encrypted_string)
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
        


# def encrypt_strings(list_of_strings):
#     for unencrypted_string in list_of_strings:
#         for c in unencrypted_string:
#             print(c)
#             encoded_char = c.encode('utf-8')

