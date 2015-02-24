from dfsm import GetIdentifierDFSM, GetNumeralDFSM, GetOperatorSeparatorDFSM
import re

def PeekFile(file):
    peek = file.read(1)
    file.seek(-1, 1)
    return peek

def main():
    source_code = open('rat_example.rat', 'r')

    tokens = []
    char = source_code.read(1)
    end_of_file = True if char == '' else False
    
    while not end_of_file:
        # Choose DFSM based on what char is
        # Let IDDFSM handle anything that starts with '_'
        if char.isalpha() or char == '_':
            dfsm = GetIdentifierDFSM()
        # Let NumeralDFSM handle anything that starts with '.'
        elif char.isdigit() or char == '.':
            dfsm = GetNumeralDFSM()
        else:
            dfsm = GetOperatorSeparatorDFSM()

        # Start building lexeme
        lexeme = char

        dfsm.Reset()
        
        # If Transition returns -1 its an epsilon transition
        #  we need to stop taking in characters and process the lexeme
        while dfsm.Transition(char) is not -1:
            # .read() return an empty string if EOF is reached
            char = source_code.read(1)
            # Check to see if EOF is reached to set end_of_file properly
            #  This prevents us from losing the last letter of the file
            if char == '':
                end_of_file = True
            lexeme += char

        # Only unget char if we aren't at EOF
        if not end_of_file:
            # This "ungets" the last character
            char = lexeme[-1]
            lexeme = lexeme[:-1]
            
        # Strips any whitespace we encounter
        while re.match(r'[\s]', char): 
            char = source_code.read(1)

        # IF peeking at the next character returns an
        # empty string we have reached EOF 
        if PeekFile(source_code) == '':
            end_of_file = True

        tokens.append((dfsm.GetToken(lexeme), dfsm))

    for token, dfsm in tokens:
        print token.type + ' -- ' + token.lexeme
     
if __name__ == '__main__':
    main()
