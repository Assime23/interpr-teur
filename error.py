# Définition de la classe de base pour les erreurs spécifiques à notre langage
class SimpleLangError(Exception):
    """
    Classe de base pour toutes les erreurs spécifiques à notre langage de programmation.
    Hérite de la classe Exception.
    """
    pass

# Définition de la classe pour les erreurs de l'analyse lexicale
class LexerError(SimpleLangError):
    """
    Classe pour les erreurs de l'analyse lexicale.
    Hérite de SimpleLangError.
    Utilisée lorsque le lexer rencontre un caractère ou une séquence inattendue.
    """
    pass

# Définition de la classe pour les erreurs de l'analyse syntaxique
class ParserError(SimpleLangError):
    """
    Classe pour les erreurs de l'analyse syntaxique.
    Hérite de SimpleLangError.
    Utilisée lorsque le parser rencontre une séquence de jetons (tokens) inattendue ou incorrecte.
    """
    pass

# Définition de la classe pour les erreurs de l'analyse sémantique
class SemanticError(SimpleLangError):
    """
    Classe pour les erreurs de l'analyse sémantique.
    Hérite de SimpleLangError.
    Utilisée lorsque l'analyse sémantique détecte des problèmes tels que des variables non déclarées,
    des types incorrects, ou des appels de fonction incorrects.
    """
    pass
