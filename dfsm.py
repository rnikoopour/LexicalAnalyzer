import transition
import re
from token import Token
keywords = [x.strip() for x in open('keywords.txt')]
class DFSM(object):
    def __init__(self, states, alphabet, trans_funcs, start_state, accept_states):
        self.states = states
        # Not using alphabet anywhere. It may be unneccesary unless we want
        #  to check the transition functions for validity or we want to
        #  check the input 
        self.alphabet = alphabet
        self.trans_funcs = trans_funcs
        self.start_state = start_state
        self.current_state = start_state
        self.accept_states = accept_states

    def Accepts(self, input):
        accepts = True
        for symbol in input:
            if symbol not in self.alphabet:
                print symbol + '-- is not in --' +self.alphabet
                accepts = False
        return accepts

    def Transition(self, symbol):
        next_state = None
        for function in self.trans_funcs:
            if function.start_state is self.current_state and \
               function.input is symbol:
                next_state = function.next_state
                break
        self.current_state = next_state
        
    def IsInAcceptingState(self, input):
        self.current_state = self.start_state
        for symbol in input:
            self.Transition(symbol)
        return True if self.current_state in self.accept_states else False

    def GetCurrentState(self):
        return self.current_state
    
    def GetToken(self, lexeme):
        return Token('Unknown', lexeme)
    
class IdentifierDFSM(DFSM):
    def Accepts(self, input):
        input = re.sub(r'[a-zA-Z]', 'l', input)
        input = re.sub(r'[0-9]', 'd', input)
        return super(IdentifierDFSM, self).Accepts(input)

    def GetToken(self, lexeme):
        token = super(IdentifierDFSM, self).GetToken(lexeme)
        input = re.sub(r'[a-zA-Z]', 'l', lexeme)
        input = re.sub(r'[0-9]', 'd', input)
        if lexeme in keywords:
            token.type = 'Keyword'
        elif self.IsInAcceptingState(input):
            token.type = 'Identifier'
        return token
        

class NumeralDFSM(DFSM):
    def Accepts(self, input):
        input = re.sub(r'[0-9]', 'd', input)
        return super(NumeralDFSM, self).Accepts(input)

    def GetToken(self, lexeme):
        token = super(NumeralDFSM, self).GetToken(lexeme)
        input = re.sub(r'[0-9]', 'd', lexeme)
        self.IsInAcceptingState(input)
        if self.GetCurrentState() is 2:
            token.type = 'Integer'
        elif self.GetCurrentState() is 3:
            token.type = 'Real'
        return token
