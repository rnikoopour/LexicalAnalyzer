'''
@mainpage Rat15S Compiler

@section intro_sec Introduction
This will become a Rat15S compiler.  Currently working on Lexical Analyzer.
@author Reza Nikoopour
@author Eric Roe
'''
from dfsm import GetIdentifierDFSM, GetNumeralDFSM, GetOperatorSeparatorDFSM
import re
import sys

def PeekFile(file):
    peek = file.read(1)
    file.seek(-1, 1)
    return peek

def Lexer(dfsm, lexeme):
    # Gets the token from the DFSM
    return dfsm.GetToken(lexeme)

def main():
    source_code = open(sys.argv[1], 'r')

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
        # The OperatorSeparatorDFSM handles everything else
        else:
            dfsm = GetOperatorSeparatorDFSM()
                
        # Start building lexeme
        lexeme = char
        # If Transition returns -1 its an epsilon transition
        #  we need to stop taking in characters and process the lexeme
        while dfsm.Transition(char) is not -1:
            char = source_code.read(1)
            # Check to see if EOF is reached to set end_of_file properly
            #  This prevents us from losing the last letter of the file
            if char == '':
                end_of_file = True
            lexeme += char
                        
        if not end_of_file:
            # This "ungets" the last char.
            if len(lexeme) > 1:
                char = lexeme[-1]
                lexeme = lexeme[:-1]
            # If len(lexeme) is 1 we need to read the next char in the file
            #  We do this because if the len of lexeme is 1 we haven't read
            #  from the file to update char
            else:
                char = source_code.read(1)

        # Strips any whitespace we encounter
        while re.match(r'[\s]', char): 
            char = source_code.read(1)

        # We need to check if after stripping whitespaces we've reached EOF
        if char == '':
            end_of_file = True

        # We don't want to add comments to the token list
        token = Lexer(dfsm, lexeme)
        if token.type is not 'Comment':
            tokens.append(token)

    output_file = open(sys.argv[2], 'w')
    output_file.write('token -- lexeme\n')
    for token in tokens:
        output_file.write(token.type + ' -- ' + token.lexeme + '\n')
    output_file.close()
     
if __name__ == '__main__':
    main()
