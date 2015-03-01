"""
@package token
This is the Token class its self explanitory
"""
class Token:
    """
    @brief This represents a token.  It has a type and a lexeme
    """
    def __init__(self, token_type, lexeme):
        """
        @brief The Constructor
        
        @param[in] token_type A string representing the token's type
        @param[in] lexeme The lexeme for the token
        """
        self.type = token_type
        self.lexeme = lexeme

    
