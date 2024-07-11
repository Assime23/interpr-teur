# Importer les modules nécessaires
import sys  # Module pour accéder aux arguments de la ligne de commande
from lexer import tokenize  # Fonction pour analyser le code source en tokens
from parser_ import Parser  # Classe pour analyser les tokens en une structure de syntaxe abstraite (AST)
from semantic_analyzer import SemanticAnalyzer  # Classe pour vérifier les erreurs sémantiques dans l'AST
from interpreter import Interpreter  # Classe pour interpréter et exécuter l'AST
from error import SimpleLangError  # Classe pour gérer les erreurs spécifiques au langage

# Fonction principale
def main():
    # Vérifier si un argument (le nom du fichier source) a été passé à la ligne de commande
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <source_file.bf>")
        return

    # Récupérer le nom du fichier source depuis les arguments de la ligne de commande
    source_file = sys.argv[1]

    # Tenter d'ouvrir et de lire le fichier source
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
     #   print(f"Erreur : Le fichier {source_file} n'a pas été trouvé.")
        return
    except IOError:
      #  print(f"Erreur : Impossible de lire le fichier {source_file}.")
        return

    # Tenter d'analyser, vérifier et interpréter le code source
    try:
        # Analyser le code source en tokens
        tokens = tokenize(code)
        # Créer un analyseur syntaxique avec les tokens et générer l'AST
        parser = Parser(tokens)
        ast = parser.parse()
        # Vérifier les erreurs sémantiques dans l'AST
        semantic_analyzer = SemanticAnalyzer(ast)
        semantic_analyzer.analyze()
        # Interpréter et exécuter l'AST
        interpreter = Interpreter(ast)
        interpreter.interpret()
    except SimpleLangError as e:
        # Afficher un message d'erreur en cas d'exception spécifique au langage
        print(f"Erreur : {e}")

# Point d'entrée du script
if __name__ == "__main__":
    main()
