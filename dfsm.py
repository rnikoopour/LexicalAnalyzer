## @package dfsm
#  This handles the description and creation of DFSMs
#
#  It includes an IdentifierDFSM, a NumeralDFSM, and an OperatorSeparatorDFSM
from transition import Transition
import re
from token import Token
keywords = [x.strip() for x in open('keywords.txt')]
id_dfsm = None
numeral_dfsm = None
operator_separator_dfsm = None

##
# @brief Returns IdentifierDFSM
#
# @return 
def GetIdentifierDFSM():
    global id_dfsm
    if id_dfsm is None:
        states = [1, 2, 3, 4]
        input_symbols = 'ld_'
        transitions = [Transition(1, 'l', 2), Transition(1, '_', 4), Transition(2, 'l', 2), Transition(2, 'd', 2), Transition(2, '_', 3), Transition(3, 'l', 2), Transition(3, 'd', 2), Transition(3, '_', 3), Transition(4, 'l', 4), Transition(4, 'd', 4), Transition(4, '_', 4)]
        start_state = states[0]
        accept_states = [states[1]]
        id_dfsm = IdentifierDFSM(states, input_symbols, transitions, start_state, accept_states)
    id_dfsm.Reset()
    return id_dfsm

def GetNumeralDFSM():
    global numeral_dfsm
    if numeral_dfsm is None:
        states = [1, 2, 3, 4]
        input_symbols = 'd.'
        transitions = [Transition(1, 'd', 2), Transition(1, '.', 4), Transition(2, 'd', 2), Transition(2, '.', 3), Transition(3, 'd', 3), Transition(3, '.', 4), Transition(4, 'd', 4), Transition(4, '.', 4)]
        start_state = states[0]
        accept_states = [states[1], states[2]]
        numeral_dfsm = NumeralDFSM(states, input_symbols, transitions, start_state, accept_states)
    numeral_dfsm.Reset()
    return numeral_dfsm

def GetOperatorSeparatorDFSM():
    global operator_separator_dfsm
    if operator_separator_dfsm is None:
        states = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        input_symbols = '@[],:{}=;()!><+-*/'
        transitions = [Transition(1, '@', 2), Transition(2, '@', 3), Transition(1, '[', 3), Transition(1, ']', 3), Transition(1,',', 3), Transition(1, ':', 4), Transition(1, '{', 3), Transition(1, '}', 3), Transition(1, '=', 6), Transition(4, '=', 5), Transition(7, '=', 8), Transition(9, '=', 8), Transition(1, ';', 3), Transition(1, '(', 3), Transition(1, ')', 3), Transition(1, '!', 7), Transition(1, '>', 8), Transition(6, '>', 8), Transition(1, '<', 9), Transition(1, '+', 5), Transition(1, '-', 5), Transition(1, '*', 5), Transition(1, '/', 5)]
        start_state = states[0]
        accept_states = [states[2], states[3], states[4], states[5], states[7], states[8]]
        operator_separator_dfsm = OperatorSeparatorDFSM(states, input_symbols, transitions, start_state, accept_states)
    operator_separator_dfsm.Reset()
    return operator_separator_dfsm

class DFSM(object):
    def __init__(self, states, alphabet, trans_funcs, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.trans_funcs = trans_funcs
        self.start_state = start_state
        self.current_state = start_state
        self.accept_states = accept_states
        self.previous_state = None

    def Reset(self):
        self.current_state = self.start_state
        self.previous_state = None
    
    def Transition(self, symbol):
        # -1 means epsilon transition
        # This means if a transition is not defined it means an epsilon transition occurs
        next_state = -1
        self.previous_state = self.current_state
        for transition in self.trans_funcs:
            #print 'State=' + str(self.current_state) + ' to use <' + str(symbol) + '>: ('+str(transition.start_state)+', '+str(transition.input)+') --> '+ str(transition.next_state)
            if transition.start_state == self.current_state and \
               transition.input == symbol:
                next_state = transition.next_state
                break
        #print 'Used: ('+symbol+', '+str(self.current_state)+') --> '+ str(next_state)
        self.current_state = next_state
        return self.current_state

    def GetToken(self, lexeme):
        return Token('Unknown', lexeme)
################################################################################
#
# END OF CLASS: DFSM
#
################################################################################
    
class IdentifierDFSM(DFSM):
    def Transition(self, input):
        input = re.sub(r'[a-zA-Z]', 'l', input)
        input = re.sub(r'[0-9]', 'd', input)
        return super(IdentifierDFSM, self).Transition(input)

    def GetToken(self, lexeme):
        token = super(IdentifierDFSM, self).GetToken(lexeme)
        input = re.sub(r'[a-zA-Z]', 'l', lexeme)
        input = re.sub(r'[0-9]', 'd', input)
        if lexeme in keywords:
            token.type = 'Keyword'
        elif self.previous_state in self.accept_states:
            token.type = 'Identifier'
        return token
        
class NumeralDFSM(DFSM):
    def Transition(self, input):
        input = re.sub(r'[0-9]', 'd', input)
        return super(NumeralDFSM, self).Transition(input)

    def GetToken(self, lexeme):
        token = super(NumeralDFSM, self).GetToken(lexeme)
        input = re.sub(r'[0-9]', 'd', lexeme)
        if self.previous_state is 2:
            token.type = 'Integer'
        elif self.previous_state is 3:
            token.type = 'Real'
        return token

class OperatorSeparatorDFSM(DFSM):
    def GetToken(self, lexeme):
        token = super(OperatorSeparatorDFSM, self).GetToken(lexeme)
        if self.previous_state in [3, 4]:
            token.type = 'Separator'
        elif self.previous_state in [6, 8, 9]:
            token.type = 'Relop'
        elif self.previous_state is 5:
            token.type = 'Operator'
        return token

