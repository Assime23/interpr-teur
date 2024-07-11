# Importer l'exception d'erreur sémantique
from error import SemanticError

# Classe principale de l'analyseur sémantique
class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast  # Arbre syntaxique abstrait (AST)
        self.variables = {}  # Dictionnaire pour stocker les variables déclarées
        self.functions = {}  # Dictionnaire pour stocker les fonctions déclarées

    # Méthode principale pour analyser l'AST
    def analyze(self):
        self.analyze_block(self.ast)

    # Méthode pour analyser un bloc d'instructions
    def analyze_block(self, block):
        for statement in block:  # Pour chaque instruction dans le bloc
            self.analyze_statement(statement)

    # Méthode pour analyser une instruction
    def analyze_statement(self, statement):
        stmt_type = statement[0]  # Type d'instruction
        if stmt_type == 'afficher':  # Instruction d'affichage
            self.analyze_expression(statement[1])
        elif stmt_type == 'variable':  # Instruction de déclaration de variable
            _, identifiant, expr = statement
            self.analyze_expression(expr)
            self.variables[identifiant] = True
        elif stmt_type == 'si':  # Instruction conditionnelle
            _, condition, true_branch, false_branch = statement
            self.analyze_expression(condition)
            self.analyze_block(true_branch)
            if false_branch:
                self.analyze_block(false_branch)
        elif stmt_type == 'tantque':  # Boucle tant que
            _, condition, body = statement
            self.analyze_expression(condition)
            self.analyze_block(body)
        elif stmt_type == 'fonction':  # Déclaration de fonction
            _, identifiant, parameters, body = statement
            self.functions[identifiant] = (parameters, body)
        elif stmt_type == 'retour':  # Instruction de retour de fonction
            self.analyze_expression(statement[1])

    # Méthode pour analyser une expression
    def analyze_expression(self, expr):
        expr_type = expr[0]  # Type d'expression
        if expr_type == 'identifier':  # Expression de variable
            _, identifiant = expr
            if identifiant not in self.variables:
                raise SemanticError(f"Variable non déclarée : {identifiant}")
        elif expr_type == 'operation':  # Expression d'opération arithmétique
            _, operator, left, right = expr
            self.analyze_expression(left)
            self.analyze_expression(right)
        elif expr_type == 'call':  # Appel de fonction
            _, identifiant, arguments = expr
            if identifiant not in self.functions:
                raise SemanticError(f"Fonction non déclarée : {identifiant}")
            parameters, body = self.functions[identifiant]
            if len(arguments) != len(parameters):
                raise SemanticError(f"Nombre d'arguments incorrect pour la fonction {identifiant}")
            for arg in arguments:
                self.analyze_expression(arg)
