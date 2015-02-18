from dfsm import IdentifierDFSM
from transition import Transition
import token
import string
import re

def GetIdentifierDFSM():
    states = [1, 2, 3]
    input_symbols = string.lowercase + string.uppercase + string.digits + '_'
    transitions = [Transition(1, 'l', 2), Transition(2, 'l', 2), Transition(2, 'd', 2), Transition(2, '_', 3), Transition(3, 'l', 2), Transition(3, 'd', 2), Transition(3, '_', 3)]
    start_state = states[0]
    accept_states = [states[1]]
    return IdentifierDFSM(states, input_symbols, transitions, start_state, accept_states)

def main():
    file = open('rat_example.rat', 'r')
    identifier_dfsm = GetIdentifierDFSM()
    tokens = []
    char = file.read(1)
    while True:
        lexeme = char
        if char.isalpha():
            while identifier_dfsm.Accepts(lexeme):
                char = file.read(1)
                # Gets us out if we reach EOF
                if not char:
                    tokens.append(identifier_dfsm.GetToken(lexeme))
                    break
                lexeme += char
            # We check if char to make sure that we have not reached EOF.
            #  This prevents us from doubling the last lexeme parsed
            if char:
                tokens.append(identifier_dfsm.GetToken(lexeme[:-1]))
                char = lexeme[-1]
        elif char.isdigit():
            print 'digit'
            char = file.read(1)
        else:
            char = file.read(1)

        if not char:
            break
    
        '''
        # If c is a whitespace char we need to read in the next character
        if re.match(r'\s', c):
            c = file.read(1)
            print c
        '''
    for token in tokens:
        print token.type + ' -- ' + token.lexeme
    
if __name__ == '__main__':
    main()
