import re
import sys

class Token:
    def __init__(id):
        self.token_id = id

keywords = [x.strip() for x in open('keywords.txt')]
operators = [x.strip() for x in open('operators.txt')]
datatypes = [x.strip() for x in open('datatypes.txt')]
separators = [x.strip() for x in open('separators.txt')] + [' ', '\n']
identifiers = {}

print keywords
print operators
print datatypes
print separators
print identifiers


def ParseToken(token):
    print token

def ParseSource(source):
    source_left = True
    current_token = source.read(1)

    # Check for empty source file
    if not current_token:
        source_left = False

    while source_left:
        next_char = source.read(1)
        if not next_char:
            ParseToken(current_token)
            break
        if next_char in separators and current_token[0] not in separators or \
           next_char not in separators and current_token[0] in separators:
            ParseToken(current_token)
            if next_char == ' ':
                next_char = source.read(1)
            current_token = next_char
        else:
            current_token += next_char

def main():
    source = open(sys.argv[1])
    ParseSource(source)
    

if __name__ == '__main__':
    main()

'''
def GetTokenInfo(word):
    if word in keywords:
        print 'keyword: ' + word
    elif word in operators:
        print 'operator: ' + word
    elif word in separators:
        print 'separator: ' + word
    elif re.match(r'\d+\.\d+', word):
        print 'real: ' + word
    elif re.match(r'\d+$', word):
        print 'integer: ' + word
    elif re.match(r'^[A-Za-z]+$', word):
        print 'identifier: ' + word
    else:
        location = len(word)
        first_symbol = ''
        for symbol in separators + operators:
            if word.find(symbol) > -1 and word.find(symbol) <= location:
                first_symbol = symbol
                location = word.find(symbol)
                print location
                print word

        print first_symbol
        if location is 0:
            location = 1
        elif location is len(word):
            location -= 1

        if first_symbol is ':=':
            location += 1
        GetTokenInfo(word[:location])
        GetTokenInfo(word[location:])
    
#filename = sys.argv[1]
#tokens = [token.strip() for token in open(filename)]
        
for token in string.split():
    GetTokenInfo(token)
'''
