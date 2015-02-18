from dfsm import IdentifierDFSM
from transition import Transition
import token
import string
import re
id_dfsm = None
numeral_dfsm = None

def GetIdentifierDFSM():
    global id_dfsm
    if id_dfsm is None:
        states = [1, 2, 3]
        input_symbols = string.lowercase + string.uppercase + string.digits + '_'
        transitions = [Transition(1, 'l', 2), Transition(2, 'l', 2), Transition(2, 'd', 2), Transition(2, '_', 3), Transition(3, 'l', 2), Transition(3, 'd', 2), Transition(3, '_', 3)]
        start_state = states[0]
        accept_states = [states[1]]
        id_dfsm = IdentifierDFSM(states, input_symbols, transitions, start_state, accept_states)
    return id_dfsm
    
def main():
    file = open('rat_example.rat', 'r')
    identifier_dfsm = GetIdentifierDFSM()
    tokens = []
    char = file.read(1)
    end_of_file = False
    
    while not end_of_file:
        if char.isalpha():
            dfsm = GetIdentifierDFSM()
        elif char.isdigit():
            char = file.read(1)
        else:
            char = file.read(1)
            
        lexeme = char
        while dfsm.Accepts(lexeme):
            char = file.read(1)
            # file.read return an empty string if EOF is reached
            if char == '':
                end_of_file = True
                break
            lexeme += char
        if not end_of_file:
            char = lexeme[-1]
            lexeme = lexeme[:-1]
            tokens.append(dfsm.GetToken(lexeme))
        else:
            tokens.append(dfsm.GetToken(lexeme))
        
        # If char is a whitespace char we need to read in the next character
        if re.match(r'\s', char):
            char = file.read(1)
            
    for token in tokens:
        print token.type + ' -- ' + token.lexeme
    
if __name__ == '__main__':
    main()
