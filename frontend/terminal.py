import traceback
import subprocess
import readline
from pprint import PrettyPrinter

from model.word import Word
from private import bybit_keys
from model import const

# import ccxt
import pybit

readline.parse_and_bind('set editing-mode emacs')

printer = PrettyPrinter()

def pprint(obj):
    printer.pprint(obj)

def clear_screen():
    subprocess.call('clear')

def main():
    clear_screen()

class LionsharkFrontend:
    def __init__(self, model) -> None:
        self.running = False
        self.model = model

        self.session = pybit.HTTP(
            endpoint="https://api.bybit.com",
            api_key=bybit_keys.API_KEY,
            api_secret=bybit_keys.API_SEC
        )
        self.ws = pybit.WebSocket(
            endpoint="wss://stream.bybit.com/realtime",
            subscriptions=["order", "position"],
            api_key=bybit_keys.API_KEY,
            api_secret=bybit_keys.API_SEC            
        )

        symbols = self.session.query_symbol()["result"]

class Terminal(LionsharkFrontend):
    def __init__(self, model) -> None:
        super().__init__(model)
    
    def run(self):
        self.running = True

        while self.running:
            commands = input().upper().split(";")
            for command in commands:
                if not command:
                    break
                    
                try:
                    self.model.parse(command)

                    if Word.is_symbol(self.model.context, symbols=self.model.symbols):
                        self._handle_symbol()
                    elif Word.is_universal(self.model.context):
                        self._handle_universal()

                except Exception as exc:
                    traceback.print_exc()
                    print(exc)
    
    def _handle_symbol(self):
        if len(self.model.words) == 1:
            self._print_symbol_information()
            return
        
        self._apply_settings()
        self._execute_current_context()
    
    def _apply_settings(self):
        for arg in self.model.args:
            if Word.is_leverage_modifier(arg):
                self._apply_symbol_leverage_settings(leverage=arg)
        
        for instantiator in (set(self.model.kwargs.keys() & set(const.INSTANTIATORS))):
            self._instantiate_variables(instantiator)
    
    def _apply_symbol_leverage_settings(self, leverage):
        self.session.set_leverage(
            symbol=self.model.context,
            buy_leverage=leverage,
            sell_leverage=leverage,
        )

    # def _instantiate_variables(instantiator):
    #     if instantiator == const.KEYWORD_RETRACE:
    #         y1, y2 = get_price_range(self.model.kwargs[instantiator])
    #         diff = y2 - y1
    #         fibs = {'f236': .236, 'f382': .382, 'f5': .5, 'f618': .618, 'f786': .786}

    #     for fibname, fibval in fibs.items():
    #         if self.model.variables.get(fo_transform._SYMBOL()) == None:
    #             model.VARIABLES[fo_transform._SYMBOL()] = {}

    #         model.VARIABLES[fo_transform._SYMBOL()][fibname] = float("{:.2f}".format(y2 - (diff * fibval)))

    def _execute_current_context(self):
        return
    
    def _handle_universal(self):
        return
    
    def _print_symbol_information(self):
        return