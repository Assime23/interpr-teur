# Classe principale de l'interpréteur
class Interpreter:
    def __init__(self, ast):
        self.ast = ast  # Arbre syntaxique abstrait (AST)
        self.variables = {}  # Dictionnaire pour stocker les variables
        self.functions = {}  # Dictionnaire pour stocker les fonctions

    # Méthode principale pour interpréter l'AST
    def interpret(self):
        self.interpret_block(self.ast)

    # Méthode pour interpréter un bloc d'instructions
    def interpret_block(self, block):
        for statement in block:  # Pour chaque instruction dans le bloc
            result = self.interpret_statement(statement)
            if result is not None:  # Gestion des retours de fonction
                return result

    # Méthode pour interpréter une instruction
    def interpret_statement(self, statement):
        stmt_type = statement[0]  # Type d'instruction
        if stmt_type == 'afficher':  # Instruction d'affichage
            expr = statement[1]
            value = self.evaluate_expression(expr)
            print(value)
        elif stmt_type == 'variable':  # Instruction de déclaration de variable
            _, identifiant, expr = statement
            value = self.evaluate_expression(expr)
            self.variables[identifiant] = value
        elif stmt_type == 'si':  # Instruction conditionnelle
            _, condition, true_branch, false_branch = statement
            if self.evaluate_expression(condition):
                return self.interpret_block(true_branch)
            elif false_branch:
                return self.interpret_block(false_branch)
        elif stmt_type == 'tantque':  # Boucle tant que
            _, condition, body = statement
            while self.evaluate_expression(condition):
                return self.interpret_block(body)
        elif stmt_type == 'fonction':  # Déclaration de fonction
            _, identifiant, parameters, body = statement
            self.functions[identifiant] = (parameters, body)
        elif stmt_type == 'retour':  # Instruction de retour de fonction
            expr = statement[1]
            return self.evaluate_expression(expr)

    # Méthode pour évaluer une expression
    def evaluate_expression(self, expr):
        expr_type = expr[0]  # Type d'expression
        if expr_type == 'number':  # Expression numérique
            return int(expr[1])
        elif expr_type == 'string':  # Expression de chaîne de caractères
            return expr[1][1:-1]  # Enlever les guillemets
        elif expr_type == 'identifier':  # Expression de variable
            return self.variables[expr[1]]
        elif expr_type == 'operation':  # Expression d'opération arithmétique
            _, operator, left, right = expr
            left_value = self.evaluate_expression(left)
            right_value = self.evaluate_expression(right)
            if operator == '+':
                return left_value + right_value
            elif operator == '-':
                return left_value - right_value
            elif operator == '*':
                return left_value * right_value
            elif operator == '/':
                return left_value / right_value
        elif expr_type == 'call':  # Appel de fonction
            _, identifiant, arguments = expr
            parameters, body = self.functions[identifiant]
            local_variables = self.variables.copy()  # Créer une copie des variables actuelles
            for param, arg in zip(parameters, arguments):
                local_variables[param] = self.evaluate_expression(arg)  # Associer les arguments aux paramètres
            previous_variables = self.variables  # Sauvegarder les variables actuelles
            self.variables = local_variables  # Remplacer les variables par les variables locales
            result = self.interpret_block(body)
            self.variables = previous_variables  # Restaurer les variables
            return result
