
CLI_PREFIX = '-> '

# General Reserved Keywords
KEYWORD_LONG = 'LONG'
KEYWORD_SHORT = 'SHORT'
KEYWORD_LIMIT = 'LIMIT'
KEYWORD_LEVERAGE = 'LEVERAGE'
KEYWORD_CANCEL = 'CANCEL'
KEYWORD_RETRACE = 'RETRACE'
KEYWORD_STOP = 'STOP'
KEYWORD_TAKE = 'TAKE'
KEYWORD_CLOSE = "CLOSE"

# Reserved Keywords for "Universal Context"
KEYWORD_CLEAR = 'CLEAR'
KEYWORD_PANIC = 'PANIC'
KEYWORD_QUIT = 'QUIT'
KEYWORD_SYMBOLS = 'SYMBOLS'
KEYWORD_VARIABLES = 'VARIABLES'
KEYWORD_POSITION = "POSITIONS"

KEYWORDS = [
    KEYWORD_LONG,
    KEYWORD_SHORT,
    KEYWORD_LIMIT,
    KEYWORD_LEVERAGE,
    KEYWORD_CANCEL,
    KEYWORD_CLOSE,
    KEYWORD_RETRACE,
    KEYWORD_STOP,
    KEYWORD_TAKE,
    KEYWORD_CLEAR,
    KEYWORD_PANIC,
    KEYWORD_QUIT,
    KEYWORD_SYMBOLS,
    KEYWORD_VARIABLES
]

"""The set of tokens in the universal context.

e.g "clear" does not require a symbol context, like "ethusdt". 

Symbol contexts are not const as they are determined from the API, 
as in the list of all the pairs offered by the exchange.
"""
UNIVERSALS = [
    KEYWORD_CLEAR, KEYWORD_QUIT, KEYWORD_PANIC, KEYWORD_SYMBOLS, KEYWORD_POSITION
]

"""The set of keywords that instatiate new variables."""
INSTANTIATORS = [
    KEYWORD_RETRACE
]
