from abc import ABC, abstractmethod
import traceback
import subprocess
import readline
from pprint import PrettyPrinter

from model.word import Word
from private import bybit_keys
from model import const
from model.model import Model

import pybit

readline.parse_and_bind('set editing-mode emacs')

printer = PrettyPrinter()

def pprint(obj):
    printer.pprint(obj)

def clear_screen():
    subprocess.call('clear')

def main():
    clear_screen()

class Lionshark(ABC):
    def __init__(self) -> None:
        self.running = False
        self.session = pybit.HTTP(
            endpoint="https://api.bybit.com",
            api_key=bybit_keys.API_KEY,
            api_secret=bybit_keys.API_SEC
        )
        self.ws = pybit.WebSocket(
            endpoint="wss://stream.bybit.com/realtime_private",
            subscriptions=["order", "position"],
            api_key=bybit_keys.API_KEY,
            api_secret=bybit_keys.API_SEC            
        )
        Word.symbols = [x["name"] for x in self.session.query_symbol()["result"]]

    @abstractmethod
    def get_input(self):
        return ""
    
    @abstractmethod
    def display_symbol_information(self, info):
        return ""
    
    def get_symbol_information(self):
        return self.session.my_position(symbol=Model.context())["result"][-1]

    def run(self):
        self.running = True

        while self.running:
            commands = self.get_input().upper().split(";")

            for command in commands:
                if not command:
                    break
                    
                try:
                    Model.parse(command)
                    if Word.is_symbol(Model.context()):
                        self._handle_symbol()
                    elif Word.is_universal(Model.context()):
                        self._handle_universal()
                except Exception as exc:
                    traceback.print_exc()
                    print(exc)
    
    def _handle_symbol(self):
        if len(Model.words) == 1:
            info = self.get_symbol_information()
            self.display_symbol_information(info)
            return

        self._apply_settings()
        self._execute_current_context()

    def _execute_current_context(self):
        if Model.side() or Model.stop_loss() or Model.take_profit():
            info = self.session.latest_information_for_symbol(symbol=Model.symbol())
            price = float(info["result"][0]["mark_price"])
            stop_loss = price * .98 if Model.side() == "Buy" else price * 1.02
            stop_loss = round(stop_loss - (stop_loss % 0.05), 3)
            take_prof = price * 1.05 if Model.side() == "Buy" else price * .95
            take_prof = round(take_prof - (take_prof % 0.05), 3)
            self.session.place_active_order(
                symbol=Model.symbol(),
                side=Model.side(),
                order_type=Model.order_type(),
                qty=Model.quantity(),
                time_in_force="GoodTillCancel",
                close_on_trigger=False,
                reduce_only=False,
                take_profit=take_prof,
                stop_loss=stop_loss,
            )

        if const.KEYWORD_CANCEL in Model.words:
            self.session.cancel_active_order(
                symbol=Model.symbol()
            )
        
        if const.KEYWORD_CLOSE in Model.words:
            self.session.close_position(symbol=Model.context())

    def _apply_settings(self):
        for arg in Model.args:
            if Word.is_leverage_modifier(arg):
                self._apply_symbol_leverage_settings(leverage=arg)
        
        for instantiator in (set(Model.kwargs.keys() & set(const.INSTANTIATORS))):
            self._instantiate_variables(instantiator)
    
    def _apply_symbol_leverage_settings(self, leverage):
        # self.session.set_leverage(symbol=Model.context(), buy_leverage=leverage, sell_leverage=leverage)
        self.session.cross_isolated_margin_switch(
            symbol=Model.context(),
            buy_leverage=leverage,
            sell_leverage=leverage,
            is_isolated=True
        )

    def _handle_universal(self):
        if Model.context() == "POSITIONS":
            positions = self.session.my_position(
                endpoint="/v2/linear/position/list"
            )
            print(positions)
            # print(self.ws.fetch("position"))
        # TODO

    # def _instantiate_variables(instantiator):
    #     if instantiator == const.KEYWORD_RETRACE:
    #         y1, y2 = get_price_range(self.model.kwargs[instantiator])
    #         diff = y2 - y1
    #         fibs = {'f236': .236, 'f382': .382, 'f5': .5, 'f618': .618, 'f786': .786}

    #     for fibname, fibval in fibs.items():
    #         if self.model.variables.get(fo_transform._SYMBOL()) == None:
    #             model.VARIABLES[fo_transform._SYMBOL()] = {}

    #         model.VARIABLES[fo_transform._SYMBOL()][fibname] = float("{:.2f}".format(y2 - (diff * fibval)))


class TerminalFrontend(Lionshark):
    def __init__(self) -> None:
        super().__init__()
    
    def get_input(self):
        return input("> ")

    def display_symbol_information(self, info):
        print(info["side"], info["size"], Model.context(), "at", str(info["leverage"]) + "x")
        print("Entry:", info["entry_price"], "| Take:", info["take_profit"], "| Stop:", info["stop_loss"], "| Liquidation:", info["liq_price"])

        # unrealized_pnl = 
        print("Unrealized PnL:")

class DiscordFrontend(Lionshark):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self):
        return ""

    def display_symbol_information(self):
        return