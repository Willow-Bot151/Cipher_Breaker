from cipherbreaker.cipherbreaker import *
import pytest

@pytest.fixture
def uncoded_strings():
    return [
        'banana',
        'everything',
        'I\'m',
        'saying',
        'right',
        'now']

@pytest.fixture
def encrypt_obj():
    return EncryptedStrings()

class CeaserCipherEncrypt():
    def test_encode_char_normal(self,encrypt_obj):
        test_char = 'a'
        test_shift = 2
        expected = 'c'
        encode_result = encrypt_obj.caeser_shift_char(
            character=test_char,
            shift=test_shift)
        assert encode_result == expected
    def test_encode_char_wrap_around(self,encrypt_obj):
        test_char = 'z'
        test_shift = 1
        expected = 'a'
        encode_result = encrypt_obj.caeser_shift_char(
            character=test_char,
            shift=test_shift)
        assert encode_result == expected
    def test_encode_char_leaves_punctuation_and_numbers(self, encrypt_obj):
        test_char1 = '1'
        test_char2 = '{'
        test_shift = 10
        encode_result = encrypt_obj.caeser_shift_char(
            character=test_char1,
            shift=test_shift)
        assert encode_result == test_char1
        encode_result = encrypt_obj.caeser_shift_char(
            character=test_char2,
            shift=test_shift)
        assert encode_result == test_char2
    def test_encode_string(self,encrypt_obj):
        test_string = "Hello, what's up?"
        expected = "Ifmmp, xibu't vq?"
        test_shift = 1
        result = encrypt_obj.caeser_shift_string(
            string=test_string,
            shift=test_shift)
        assert result == expected

class TestVignereCipherEncrypt():
    def test_encode_string_long_key_no_spaces(self):
        test_key = 'abc'
        test_string = 'dog'
        expected = 'dpi'
        test_cipher = EncryptedStrings()
        result = test_cipher.Vigenere_cipher_encrypt_string(
            string=test_string,
            key=test_key)
        assert result == expected
    def test_encode_string_long_key(self):
        test_key = 'oculorhinolaryngology'
        test_string = 'attacking tonight'
        expected = 'ovnlqbpvt hznzeuz'
        test_cipher = EncryptedStrings()
        result = test_cipher.Vigenere_cipher_encrypt_string(
            string=test_string,
            key=test_key)
        assert result == expected
    def test_encode_string_repeated_key(self):
        test_key = 'abcd'
        test_string = 'burger'
        expected = 'bvtjes'
        test_cipher = EncryptedStrings()
        result = test_cipher.Vigenere_cipher_encrypt_string(
            string=test_string,
            key=test_key)
        assert result == expected



class TestCeaserCipherBreaker():
    def test_decrypt_string(self):
        test_string = "Ifmmp, xibu't vq?"
        expected = "Hello, what's up?"
    def test_find_proportion_of_common_words(self):
        test_string1 = "A big dinner"
        test_string2 = "Grrb Agagaga Ggrubbul"
        test_breaker = CipherBreaker()
        assert test_breaker.find_proportion_of_common_words_in_a_string(
            string=test_string1
        ) == 1
        assert test_breaker.find_proportion_of_common_words_in_a_string(
            string=test_string2
        ) == 0
    def test_order_by_amount_of_common_words(self):
        test_string_list = [
            "I'm poopoo de grande",
            "I don't know honey",
            "I don't know hunny",
            "I want a cigarette"
        ]
        test_breaker = CipherBreaker()
        assert test_breaker.order_by_amount_of_common_words(
            test_string_list)[0] == "I want a cigarette"
    def test_caeser_shift_decrypt(self):
        test_string = "made"
        expected_first = "nbef"
        expected_last = "lzcd"
        test_breaker = CipherBreaker()
        result = test_breaker.caeser_shift_decrypt(test_string)
        assert result[0] == test_string
        assert result[1] == expected_first
        assert result[-1:][0] == expected_last




