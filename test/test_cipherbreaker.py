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

class TestVigenereCipherBreaker():
    @pytest.mark.skip
    def test_vigenere_cipher_decrypt(self):
        test_string = 'CSASTPKVSIQUTGQUCSASTPIUAQJB'
        test_breaker = CipherBreaker()
        result = test_breaker.vigenere_cipher_decrypt_kasiski_test(test_string)
        assert result == {
            'key' : 'ABCDABCDABCDABCDABCDABCDABCD',
            'text' : 'cryptoisshortforcryptography'
        }
    def test_strip_whitespace(self):
        test_string = 'dog dog \ndog\tdog'
        expected = 'dogdogdogdog'
        test_breaker = CipherBreaker()
        assert test_breaker.strip_whitespace(test_string) == expected
    def test_find_substrings(self):
        test_string = 'chfafblbltoeiwkhnnwchfaf'
        test_breaker = CipherBreaker()
        result = test_breaker.find_all_substrings(test_string)
        assert 'chfaf' in result
        assert 'abababa' not in result
    # def test_find_repeats_substring(self):
    #     test_string = 'chfafblbltoeiwkhnnwchfaf'
    #     test_breaker = CipherBreaker()
    #     result = test_breaker.find_repeats_of_substrings(test_string)
    #     assert result == {
    #         'chfaf' : 2,
    #         'chfa' : 2,
    #         'hfaf' : 2,
    #         'chf' : 2,
    #         'hfa' : 2,
    #         'faf' : 2
    #     }
    def test_record_position_of_repeated_substring(self):
        test_string = 'chfafblbltoeiwkhnnwchfaf'
        test_substring = 'faf'
        expected = [(2,5),(21,24)]
        test_breaker = CipherBreaker()
        result = test_breaker.record_position_of_repeated_substrings(
            substring=test_substring,
            string=test_string
        )
        assert result == expected
    def test_count_substrings(self):
        test_string = 'chfafblbltoeiwkhnnwchfaf'
        test_substring = 'faf'
        expected = 2
        test_breaker = CipherBreaker()
        result = test_breaker.count_occurances_of_substring(
            substring=test_substring,
            string=test_string
        )
        assert result == expected
    def test_calculate_distances_berween_substrings(self):
        test_positions = [(2,5),(21,24)]
        expected = [19]
        test_breaker = CipherBreaker()
        result = test_breaker.calculate_distances_between_substrings(
            positions=test_positions
        )
        assert result == expected
    def test_calculate_distances_many_occurances(self):
        test_positions = [(2,5),(8,11),(14,17),(21,24)]
        expected = [6,6,19,12,13,7]
        expected.sort()
        test_breaker = CipherBreaker()
        result = test_breaker.calculate_distances_between_substrings(
            positions=test_positions
        )
        assert result == expected
    def test_find_repeats_substring(self):
        test_string = 'chfafblbltoeiwkhnnwfaftoe'
        test_breaker = CipherBreaker()
        result = test_breaker.find_repeats_of_substrings(test_string)
        expected = {
            'faf' : {
                'repeats' : 2,
                'distances' : [17]
            },
            'toe' : {
                'repeats' : 2,
                'distances' : [13]
            }
        }
        assert result == expected
    def test_find_factors(self):
        test_number = 604
        test_limit = 200
        expected1 = [1,2,4,151]
        expected2 = [1,2,4,151,302,604]
        test_breaker = CipherBreaker()
        result1 = test_breaker.find_factors_up_to_limit_of_an_integer(
            test_number,
            test_limit)
        result2 = test_breaker.find_factors_up_to_limit_of_an_integer(test_number)
        assert result1 == expected1
        assert result2 == expected2 

    @pytest.mark.skip
    def test_big(self):
        test_string = """
CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGV
DURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGX
CFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQ
BESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUW
LBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBT
NAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVU
FFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCT
HLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFP
LLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREY
IJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVF
UQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUK
YHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGO
FZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZX
HUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFY
UWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAI
XZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXY
KZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA
"""
        test_breaker = CipherBreaker()
        test_breaker.find_repeats_of_substrings(test_string)
        assert False

@pytest.fixture
def test_breaker():
    return CipherBreaker()

class TestWeighting():
    def test_weighting1(self,test_breaker):
        test_string = """
CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGV
DURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGX
CFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQ
BESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUW
LBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBT
NAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVU
FFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCT
HLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFP
LLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREY
IJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVF
UQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUK
YHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGO
FZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZX
HUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFY
UWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAI
XZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXY
KZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA
"""
        test1_input = test_breaker.find_repeats_of_substrings(
            test_breaker.strip_whitespace(test_string))
        result = test_breaker.decide_key_length(test1_input)
        expected = 6
        assert result == 6
    def test_weighting2(self,test_breaker):
        test_string = 'VHVSSPQUCEMRVBVBBBVHVSURQGIBDUGRNICJQUCERVUAXSSR'
        test1_input = test_breaker.find_repeats_of_substrings(
            test_breaker.strip_whitespace(test_string))
        result = test_breaker.decide_key_length(test1_input)
        assert result == 6
    @pytest.mark.skip
    def test_weighting3(self,test_breaker):
        test_string = 'lippsXtvsjiwwsvXlsaXeviXcsyXkmziXqiXqcXxirXkvehiXmjXcsyXjmrhXqcXewwmkrqirxXywijypXxleroXcsyXwsXqyglXX'
        test1_input = test_breaker.find_repeats_of_substrings(
            test_breaker.strip_whitespace(test_string))
        result = test_breaker.decide_key_length(test1_input)
        assert result == 6

class TestFrequencyAnalysis():
    def test_frequency_analysis1(self, test_breaker):
        test_string = """
LIVITCSWPIYVEWHEVSRIQMXLEYVEOIEWHRXEXIPFEMVEWHKVSTYLXZIXLIKIIXPIJVSZEYPERRGERIM
WQLMGLMXQERIWGPSRIHMXQEREKIETXMJTPRGEVEKEITREWHEXXLEXXMZITWAWSQWXSWEXTVEPMRXRSJ
GSTVRIEYVIEXCVMUIMWERGMIWXMJMGCSMWXSJOMIQXLIVIQIVIXQSVSTWHKPEGARCSXRWIEVSWIIBXV
IZMXFSJXLIKEGAEWHEPSWYSWIWIEVXLISXLIVXLIRGEPIRQIVIIBGIIHMWYPFLEVHEWHYPSRRFQMXLE
PPXLIECCIEVEWGISJKTVWMRLIHYSPHXLIQIMYLXSJXLIMWRIGXQEROIVFVIZEVAEKPIEWHXEAMWYEPP
XLMWYRMWXSGSWRMHIVEXMSWMGSTPHLEVHPFKPEZINTCMXIVJSVLMRSCMWMSWVIRCIGXMWYMX"""
        expected = """
hereuponlegrandarosewithagraveandstatelyairandbroughtmethebeetlefromaglasscasei
nwhichitwasencloseditwasabeautifulscarabaeusandatthattimeunknowntonaturalistsof
courseagreatprizeinascientificpointofviewthereweretworoundblackspotsnearoneextr
emityofthebackandalongoneneartheotherthescaleswereexceedinglyhardandglossywitha
lltheappearanceofburnishedgoldtheweightoftheinsectwasveryremarkableandtakingall
thingsintoconsiderationicouldhardlyblamejupiterforhisopinionrespectingit"""
        assert test_breaker.frequency_analysis(test_string) == expected