# Importer l'exception d'erreur de l'analyseur syntaxique
from error import ParserError

# Classe principale de l'analyseur syntaxique
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Liste des jetons à analyser
        self.pos = 0  # Position actuelle dans la liste des jetons

    # Méthode principale pour analyser les jetons
    def parse(self):
        instructions = []
        while self.pos < len(self.tokens):  # Tant qu'il y a des jetons à analyser
            instructions.append(self.parse_instruction())  # Analyser une instruction et l'ajouter à la liste
        return instructions

    # Méthode pour analyser une instruction
    def parse_instruction(self):
        if self.pos >= len(self.tokens):  # Si on est à la fin des jetons
            raise ParserError("Fin inattendue des jetons")
        token_type, lexeme = self.tokens[self.pos]  # Récupérer le type de jeton et son lexème
        if token_type == 'KEYWORD':  # Si le jeton est un mot-clé
            if lexeme == 'afficher':
                return self.parse_instruction_afficher()
            elif lexeme == 'variable':
                return self.parse_instruction_variable()
            elif lexeme == 'si':
                return self.parse_instruction_si()
            elif lexeme == 'tantque':
                return self.parse_instruction_tantque()
            elif lexeme == 'fonction':
                return self.parse_instruction_fonction()
            elif lexeme == 'retour':
                return self.parse_instruction_retour()
        raise ParserError(f"Jeton inattendu : {lexeme}")

    # Méthode pour analyser l'instruction 'afficher'
    def parse_instruction_afficher(self):
        self.pos += 1  # Consommer 'afficher'
        expr = self.parse_expression()  # Analyser l'expression suivante
        return ('afficher', expr)

    # Méthode pour analyser l'instruction de déclaration de variable
    def parse_instruction_variable(self):
        self.pos += 1  # Consommer 'variable'
        token_type, identifiant = self.tokens[self.pos]
        if token_type != 'IDENTIFIER':
            raise ParserError(f"Identifiant attendu, trouvé : {token_type}")
        self.pos += 1  # Consommer l'identifiant
        if self.tokens[self.pos][1] != '=':
            raise ParserError(f"'=' attendu, trouvé : {self.tokens[self.pos][1]}")
        self.pos += 1  # Consommer '='
        expr = self.parse_expression()  # Analyser l'expression suivante
        return ('variable', identifiant, expr)

    # Méthode pour analyser l'instruction conditionnelle 'si'
    def parse_instruction_si(self):
        self.pos += 1  # Consommer 'si'
        condition = self.parse_expression()  # Analyser l'expression de condition
        if self.tokens[self.pos][1] != '{':
            raise ParserError(f"{{ attendu, trouvé : {self.tokens[self.pos][1]}")
        self.pos += 1  # Consommer '{'
        true_branch = []
        while self.tokens[self.pos][1] != '}':  # Analyser le bloc de code 'vrai'
            true_branch.append(self.parse_instruction())
        self.pos += 1  # Consommer '}'
        false_branch = None
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'sinon':  # Vérifier s'il y a un bloc 'sinon'
            self.pos += 1  # Consommer 'sinon'
            if self.tokens[self.pos][1] != '{':
                raise ParserError(f"{{ attendu, trouvé : {self.tokens[self.pos][1]}")
            self.pos += 1  # Consommer '{'
            false_branch = []
            while self.tokens[self.pos][1] != '}':  # Analyser le bloc de code 'faux'
                false_branch.append(self.parse_instruction())
            self.pos += 1  # Consommer '}'
        return ('si', condition, true_branch, false_branch)

    # Méthode pour analyser la boucle 'tantque'
    def parse_instruction_tantque(self):
        self.pos += 1  # Consommer 'tantque'
        condition = self.parse_expression()  # Analyser l'expression de condition
        if self.tokens[self.pos][1] != '{':
            raise ParserError(f"{{ attendu, trouvé : {self.tokens[self.pos][1]}")
        self.pos += 1  # Consommer '{'
        body = []
        while self.tokens[self.pos][1] != '}':  # Analyser le bloc de code du corps de la boucle
            body.append(self.parse_instruction())
        self.pos += 1  # Consommer '}'
        return ('tantque', condition, body)

    # Méthode pour analyser la déclaration de fonction
    def parse_instruction_fonction(self):
        self.pos += 1  # Consommer 'fonction'
        token_type, identifiant = self.tokens[self.pos]
        if token_type != 'IDENTIFIER':
            raise ParserError(f"Identifiant attendu pour le nom de la fonction, trouvé : {token_type}")
        self.pos += 1  # Consommer l'identifiant
        if self.tokens[self.pos][1] != '(':
            raise ParserError(f"'(' attendu, trouvé : {self.tokens[self.pos][1]}")
        self.pos += 1  # Consommer '('
        parameters = []
        while self.tokens[self.pos][1] != ')':  # Analyser les paramètres de la fonction
            if self.tokens[self.pos][0] != 'IDENTIFIER':
                raise ParserError(f"Identifiant attendu pour les paramètres, trouvé : {self.tokens[self.pos][0]}")
            parameters.append(self.tokens[self.pos][1])
            self.pos += 1
            if self.tokens[self.pos][1] == ',':
                self.pos += 1  # Consommer ','
        self.pos += 1  # Consommer ')'
        if self.tokens[self.pos][1] != '{':
            raise ParserError(f"{{ attendu, trouvé : {self.tokens[self.pos][1]}")
        self.pos += 1  # Consommer '{'
        body = []
        while self.tokens[self.pos][1] != '}':  # Analyser le bloc de code du corps de la fonction
            body.append(self.parse_instruction())
        self.pos += 1  # Consommer '}'
        return ('fonction', identifiant, parameters, body)

    # Méthode pour analyser l'instruction de retour
    def parse_instruction_retour(self):
        self.pos += 1  # Consommer 'retour'
        expr = self.parse_expression()  # Analyser l'expression suivante
        return ('retour', expr)

    # Méthode pour analyser une expression
    def parse_expression(self):
        left = self.parse_simple_expression()  # Analyser une expression simple
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OPERATOR':
            operator = self.tokens[self.pos][1]
            self.pos += 1  # Consommer l'opérateur
            right = self.parse_simple_expression()
            left = ('operation', operator, left, right)  # Combiner les expressions avec l'opérateur
        return left

    # Méthode pour analyser une expression simple
    def parse_simple_expression(self):
        token_type, lexeme = self.tokens[self.pos]
        if token_type == 'NUMBER':  # Si l'expression est un nombre
            self.pos += 1
            return ('number', lexeme)
        elif token_type == 'IDENTIFIER':  # Si l'expression est un identifiant
            self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos][1] == '(':
                return self.parse_function_call(lexeme)  # Appel de fonction
            return ('identifier', lexeme)
        elif token_type == 'STRING':  # Si l'expression est une chaîne de caractères
            self.pos += 1
            return ('string', lexeme)
        raise ParserError(f"Jeton inattendu dans la simple expression : {lexeme}")

    # Méthode pour analyser un appel de fonction
    def parse_function_call(self, identifiant):
        self.pos += 1  # Consommer '('
        arguments = []
        while self.tokens[self.pos][1] != ')':  # Analyser les arguments de la fonction
            arguments.append(self.parse_expression())
            if self.tokens[self.pos][1] == ',':
                self.pos += 1  # Consommer ','
        self.pos += 1  # Consommer ')'
        return ('call', identifiant, arguments)
