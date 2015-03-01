"""
@package dfsm
This handles the description and creation of DFSMs

It includes an IdentifierDFSM, a NumeralDFSM, and an OperatorSeparatorDFSM
"""
from transition import Transition
import re
from token import Token

## Keywords of the language
keywords = [x.strip() for x in open('keywords.txt')]
## Holds the IdentifierDFSM
id_dfsm = None
## Holds the NumeralDFSM
numeral_dfsm = None
## Holds the OperatorSeparatorDFSM
operator_separator_dfsm = None

def GetIdentifierDFSM():
    """
    @brief Returns the IdentifierDFSM
    
    @return Returns the singleton @ref id_dfsm which is an IdentifierDFSM in its starting state
    """
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
    """
    @brief Returns the NumeralDFSM

    @return Returns the singleton @ref numeral_dfsm which is NumeralDFSM in its starting state
    """
    global numeral_dfsm
    if numeral_dfsm is None:
        states = [1, 2, 3, 4]
        input_symbols = 'd.'
        transitions = [Transition(1, 'd', 2), Transition(1, '.', 4), Transition(2, 'd', 2), Transition(2, '.', 5), Transition(3, 'd', 3), Transition(3, '.', 4), Transition(4, 'd', 4), Transition(4, '.', 4), Transition(5, 'd', 3), Transition(5, '.', 4)]
        start_state = states[0]
        accept_states = [states[1], states[2]]
        numeral_dfsm = NumeralDFSM(states, input_symbols, transitions, start_state, accept_states)
    numeral_dfsm.Reset()
    return numeral_dfsm


def GetOperatorSeparatorDFSM():
    """
    @brief Returns the OperatorSeparatorDFSM
    
    @return Returns the singleton @ref operator_separator_dfsm which is OperatorSeparatorDFSM in its starting state
    """
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
    """
    @brief Base class for DFSMs

    No DFSM objects should be created.  This should just be used so custom DFSM objects have the same interface.
    """
    def __init__(self, states, alphabet, trans_funcs, start_state, accept_states):
        """
        @brief The Constructor
        
        @param[in] states A list of possible states
        @param[in] alphabet A string of the symbols the DFSM should recognize
        @param[in] trans_funcs A list of transition functions
        @param[in] start_state The state the DFSM should start in
        @param[in] accept_states A list containing accepting states
        """
        self.states = states
        self.alphabet = alphabet
        self.trans_funcs = trans_funcs
        self.start_state = start_state
        self.current_state = start_state
        self.accept_states = accept_states
        self.previous_state = None

    def Reset(self):
        """
        @brief Resets DFSM to original state
        """
        self.current_state = self.start_state
        self.previous_state = None
    
    def Transition(self, symbol):
        """
        @brief Updates current state based on the incoming symbol
      
        Search through transitions for transition matching current state and symbol and switch to that state.  If no transition is found current_state is set to -1
        @param[in] symbol A string 1 char long
        @return Returns the current state of the machine.  Epsilon tranisitions are represented by a return value of -1
        @post The DFSM's previous_state is updated to the current_state. The DFSM's current_state member is updated to the newest state. 
        """
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
        '''
        @brief Returns an unidentified token

        @param[in] lexeme A string representing the token's lexeme
        @return Returns a Token object with the token type set to "Unknown"
        '''
        return Token('Unknown', lexeme)
    
class IdentifierDFSM(DFSM):
    """
    @brief DFSM that can identify Identifiers and Keywords in the Langauge.
    """
    def Transition(self, input):
        """
        @brief Updates current state based on the incoming symbol.

        All alpha characters and turned into 'l'. All digit characters are turned into 'd'. Then DFSM.Transition() is called
        Changing alpha and digit chars into 'l' and 'd' allows us simplify the alphabet.
        @param[in] symbol A string 1 char long
        @return Returns the current state of the machine.  Epsilon tranisitions are represented by a return value of -1
        @post The DFSM's previous_state is updated to the current_state. The DFSM's current_state member is updated to the newest state. 
        """
        input = re.sub(r'[a-zA-Z]', 'l', input)
        input = re.sub(r'[0-9]', 'd', input)
        return super(IdentifierDFSM, self).Transition(input)

    def GetToken(self, lexeme):
        '''
        @brief Returns a token identifying lexeme

        @param[in] lexeme A string representing the token's lexeme
        @return Returns a Token object with the type set properly.  If lexeme is keyword, Token.type = 'keyword'.  If IdentifierDFSM.previous_state is an accepting state and lexeme is not a keyword, Token.type = 'identifier'.  If IdentifierDFSM is not in accepting state then Token.type = 'Unknown'.
        '''
        token = super(IdentifierDFSM, self).GetToken(lexeme)
        if lexeme in keywords and self.previous_state in self.accept_states:
            token.type = 'Keyword'
        elif self.previous_state in self.accept_states:
            token.type = 'Identifier'
        return token
        
class NumeralDFSM(DFSM):
    """
    @brief DFSM that can identify Ints and Reals in the Langauge.
    """
    def Transition(self, input):
        """
        @brief Updates current state based on the incoming symbol.

        All digit characters are turned into 'd'. Then DFSM.Transition() is called
        Changing digits to 'd' allows us to simplify the alphabet.
        @param[in] symbol A string 1 char long
        @return Returns the current state of the machine.  Epsilon tranisitions are represented by a return value of -1
        @post The DFSM's previous_state is updated to the current_state. The DFSM's current_state member is updated to the newest state. 
        """
        input = re.sub(r'[0-9]', 'd', input)
        return super(NumeralDFSM, self).Transition(input)

    def GetToken(self, lexeme):
        """
        @brief Returns a token identifying lexeme

        @param[in] lexeme A string representing the token's lexeme
        @return Returns a Token object with the type set properly.  If NumeralDFSM.previous_state = 2, Token.type = 'Integer'. If NumeralDFSM.previous_state = 3, Token.type = 'Real' .  If NumeralDFSM is not in accepting state then lexeme is unidentified.
        """
        token = super(NumeralDFSM, self).GetToken(lexeme)
        if self.previous_state is 2:
            token.type = 'Integer'
        elif self.previous_state is 3:
            token.type = 'Real'
        return token

class OperatorSeparatorDFSM(DFSM):
    """
    @brief DFSM that can identify Separators and Operators in the language
    """
    def GetToken(self, lexeme):
        """
        @brief Returns a token identifying lexeme

        @param[in] lexeme A string representing the token's lexeme
        @return Returns a Token object with the type set properly.  If OperatorSeparatorDFSM.previous_state = 3 or 4, Token.type = 'Separator'.  If OperatorSeparatorDFSM.previous_state = 6, 8, or 9, Token.type = 'Relop'. If OperatorSeparatorDFSM.previous_state = 5, Token.type = 'Operator'.  If OperatorSeparatorDFSM is not in accepting state then lexeme is unidentified.
        """
        token = super(OperatorSeparatorDFSM, self).GetToken(lexeme)
        if self.previous_state in [3, 4]:
            token.type = 'Separator'
        elif self.previous_state in [6, 8, 9]:
            token.type = 'Relop'
        elif self.previous_state is 5:
            token.type = 'Operator'
        return token

