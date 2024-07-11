# Importer les modules nécessaires
import re  # Module pour les expressions régulières
from grammar import Grammar  # Classe contenant la définition de la grammaire
from error import LexerError  # Classe pour gérer les erreurs spécifiques au lexer

# Fonction pour analyser le code source en tokens
def tokenize(code):
    tokens = []  # Liste pour stocker les tokens générés
    while code:  # Tant qu'il reste du code à analyser
        match = None  # Initialiser la variable match à None
        # Parcourir tous les types de tokens et leurs motifs correspondants
        for token_type, pattern in Grammar.TOKEN_TYPES.items():
            regex = re.compile(pattern)  # Compiler l'expression régulière
            match = regex.match(code)  # Tenter de faire correspondre le début du code avec l'expression régulière
            if match:  # Si une correspondance est trouvée
                lexeme = match.group(0)  # Extraire le lexème correspondant
                # Vérifier si le lexème est un mot-clé
                if token_type == 'IDENTIFIER' and lexeme in Grammar.KEYWORDS:
                    token_type = 'KEYWORD'
                # Ignorer les espaces blancs
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, lexeme))  # Ajouter le token à la liste des tokens
                code = code[len(lexeme):]  # Supprimer le lexème du début du code
                break  # Sortir de la boucle for et commencer à chercher le prochain token
        if not match:  # Si aucune correspondance n'est trouvée
            raise LexerError(f"Caractère inattendu : {code[0]}")  # Lever une erreur de lexer
    return tokens  # Retourner la liste des tokens générés
