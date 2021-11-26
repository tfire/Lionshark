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

    def parse(self, command):
        words = command.strip().split()
        self.words = words

        invalid = lambda word: not Word.is_valid(word)
        if any(list(filter(invalid, words))):
            raise Exception("Invalid words: " + str(list(filter(invalid, words))))

        self.args = list(filter(Word.is_arg, words[1:]))
        self.kwargs = {
            word.split("=")[0]: word.split("=") for word in \
            list(filter(Word.is_keyword, words))
        }

    @property
    def context(self):
        if self.words:
            return self.words[0]
        
        return None

model = Model()