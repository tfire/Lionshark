from model import const

from model.word import Word

class Model:
    """The pairs of tickers that enable an instrument context."""
    symbols = []
    """The current ordered set of words in the last command."""
    words = []
    """Variables created and referencable by the interpreter."""
    variables = {}
    """Words in the command without a keyword= format."""
    args = []
    """Words in the command that were found to have a keyword= format."""
    kwargs = {}

    @staticmethod
    def parse(command):
        words = command.strip().split()
        Model.words = words

        invalid = lambda word: not Word.is_valid(word)
        if any(list(filter(invalid, words))):
            raise Exception("Invalid words: " + str(list(filter(invalid, words))))

        Model.args = list(filter(Word.is_arg, words[1:]))
        Model.kwargs = {
            word.split("=")[0]: word.split("=") for word in \
            list(filter(Word.is_keyword, words))
        }

    @staticmethod
    def context():
        if Model.words:
            return Model.words[0]
        return None
    
    @staticmethod
    def universal():
        if not Word.is_universal(Model.context()):
            raise Exception("No universal in this command.")
        return Model.context()
    
    @staticmethod
    def symbol():
        if not Word.is_symbol(Model.context()):
            raise Exception("No symbol in this context.")
        return Model.context()
    
    @staticmethod
    def order_type():
        if const.KEYWORD_LIMIT in Model.kwargs:
            return "Limit"
        if const.KEYWORD_LONG in Model.args or const.KEYWORD_SHORT in Model.args:
            return "Market"
        return None

    @staticmethod
    def side():
        if const.KEYWORD_LONG in Model.args and const.KEYWORD_SHORT in Model.args:
            return None
        if const.KEYWORD_LONG in Model.args:
            return "Buy"
        if const.KEYWORD_SHORT in Model.args:
            return "Sell"
        
        return None
    
    @staticmethod
    def quantity():
        quantities = list(filter(Word.is_number, Model.words))
        if len(quantities) == 1:
            return quantities[0]
        return None
    
    @staticmethod
    def stop_loss():
        return Model.kwargs.get(const.KEYWORD_STOP)
    
    @staticmethod
    def take_profit():
        return Model.kwargs.get(const.KEYWORD_TAKE)
    
