from .TunerStudioIniPreProcessor import TsIniPreProcessor
from .TreeLexer import TreeLexerAdapter
from lark import Lark, Tree, Transformer
from pathlib import Path

_GRAMMAR = Path(__file__).parent / 'ts_ini.lark'
_GRAMMAR_CACHE = _GRAMMAR.with_suffix('.lark.cache')

class TsIniParser:
    """TunerStudio INI file parser
    
    This parser is slightly less tolerant than TunerStudio:
     key-value pairs: the values must be comma delimited (TunerStudio tolerates spaces)
     there must be a blank line at the end
     Expression markers ("{", "}") and parentheses must be balanced
     All identifiers must be cnames (no spaces, quotes etc.)
    """

    class transform_terminals(Transformer):
        """Process terminal tokens"""
        def KEY(self, token):
            return token.update(value=token.value.rstrip(' ='))
        def NUMBER_FIELD(self, token):
            return token.update(value=float(token.value))
        def DECIMAL_INT_CONSTANT(self, token):
            return token.update(value=int(token.value))        
        def BINARY_INT_CONSTANT(self, token):
            return token.update(value=int(token.value, 2))
        def HEX_CONSTANT(self, token):
            return token.update(value=int(token.value, 16))
        def FLOATING_CONSTANT(self, token):
            return token.update(value=float(token.value))   

    def __init__(self):
        self._pre_processor = TsIniPreProcessor()
        self._ts_parser = Lark.open(_GRAMMAR, parser='lalr', debug = True, cache = str(_GRAMMAR_CACHE), transformer = TsIniParser.transform_terminals())
        # Adapt the parser lexer to consume the preprocessor output (a Tree)
        self._ts_parser.parser.lexer = TreeLexerAdapter(self._ts_parser.parser.lexer)

    def define(self, symbol:str, value):
        """Define a preprocessor symbol to control preprocessing condtionals

        Equivalent of #set in the INI file. E.g.
          #set CAN_COMMANDS
        becomes
          define('CAN_COMMANDS', True)
        """
        
        self._pre_processor.define(symbol, value)

    def on_error(self, e):
        pass

    def parse(self, input, on_error=None) -> Tree:
        return self._ts_parser.parse(self._pre_processor.pre_process(input, on_error=self.on_error), on_error=self.on_error)