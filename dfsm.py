import transition
import re

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
        self.current_state = self.start_state
        for symbol in input:
            self.Transition(symbol)
        return self.IsInAcceptingState()

    def Transition(self, symbol):
        next_state = None
        for function in self.trans_funcs:
            if function.start_state is self.current_state and \
               function.input is symbol:
                print str(function.start_state) + ' -> ' + symbol + ' == ' +  str(function.next_state)
                next_state = function.next_state
                break
        self.current_state = next_state
        
    def IsInAcceptingState(self):
        return True if self.current_state in self.accept_states else False

class IdentifierDFSM(DFSM):
    def Accepts(self, input):
        input = re.sub(r'[a-zA-Z]', 'l', input)
        input = re.sub(r'[0-9]', 'd', input)
        return super(IdentifierDFSM, self).Accepts(input)
