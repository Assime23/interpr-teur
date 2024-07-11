# Définition de la classe Grammar
class Grammar:
    # Liste des mots-clés du langage
    KEYWORDS = ['afficher', 'variable', 'si', 'sinon', 'tantque', 'fonction', 'retour']
    
    # Liste des opérateurs utilisés dans le langage
    OPERATORS = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
    
    # Liste des caractères de ponctuation utilisés dans le langage
    PUNCTUATION = ['{', '}', '(', ')', ',']
    
    # Définition des types de jetons (tokens) avec leurs expressions régulières correspondantes
    TOKEN_TYPES = {
        'NUMBER': r'\d+',  # Expression régulière pour les nombres
        'STRING': r'"[^"]*"',  # Expression régulière pour les chaînes de caractères entre guillemets
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',  # Expression régulière pour les identifiants (lettres, chiffres, underscores)
        'OPERATOR': r'==|!=|<=|>=|[+\-*/=<>]',  # Expression régulière pour les opérateurs
        'KEYWORD': r'\b(' + '|'.join(KEYWORDS) + r')\b',  # Expression régulière pour les mots-clés
        'PUNCTUATION': r'[' + ''.join(PUNCTUATION) + r']',  # Expression régulière pour la ponctuation
        'WHITESPACE': r'\s+'  # Expression régulière pour les espaces blancs
    }
