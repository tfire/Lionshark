from model import const

class Word:
    symbols = []
    
    @staticmethod
    def is_valid(word):
        return any([
            Word.is_range(word),
            Word.is_quantity(word),
            Word.is_symbol(word),
            Word.is_keyword(word),
            Word.is_universal(word),
            Word.is_kwarg(word),
            Word.is_leverage_modifier(word),
        ])

    @staticmethod
    def is_symbol(word):
        return word in Word.symbols

    @staticmethod
    def is_universal(word):
        return word in const.UNIVERSALS
    
    @staticmethod
    def is_keyword(word):
        return word in const.KEYWORDS

    @staticmethod
    def is_leverage_modifier(word):
        return word[-1] == "X"

    @staticmethod
    def is_quantity(word):
        return any([
            Word.is_relative_value(word),
            Word.is_number(word),
            Word.is_variable(word)
        ])

    @staticmethod
    def is_number(word):
        try:
            float(word)
            return True
        except:
            return False

    @staticmethod
    def is_relative_value(word):
        return word[-1] == "%"
    
    @staticmethod
    def is_variable(word):
        return word 

    @staticmethod
    def is_arg(word):
        return len(word.split("=")) == 1

    @staticmethod
    def is_kwarg(word):
        return len(word.split('=')) == 2 and Word.is_keyword(word)
    
    @staticmethod
    def is_range(word):
        subwords = word.split("-")
        if len(subwords) == 2 and any(list(map(Word.is_valid, subwords))):
            return True
        
        return False
    