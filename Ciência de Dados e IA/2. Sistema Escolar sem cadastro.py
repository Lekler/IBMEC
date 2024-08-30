class Aluno:
    def __init__(self, nome, idade, matricula):
        self.nome = nome
        self.idade = idade
        self.matricula = matricula
        self.materias = {}

    def matricular_materia(self, materia):
        if materia not in self.materias:
            self.materias[materia] = []
            print(f"Aluno {self.nome} matriculado em {materia}.")
        else:
            print(f"Aluno {self.nome} já está matriculado em {materia}.")

    def adicionar_nota(self, materia, nota):
        if materia in self.materias:
            self.materias[materia].append(nota)
            print(f"Nota {nota} adicionada em {
                  materia} para o aluno {self.nome}.")
        else:
            print(f"Aluno {self.nome} não está matriculado em {materia}.")

    def exibir_boletim(self):
        print(f"Boletim de {self.nome}:")
        for materia, notas in self.materias.items():
            print(f"Matéria: {materia} - Notas: {notas}")

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Matrícula: {self.matricula}")
        self.exibir_boletim()


class SistemaCadastro:
    def __init__(self):
        self.alunos = {}

    def cadastrar_aluno(self, nome, idade, matricula):
        if matricula not in self.alunos:
            novo_aluno = Aluno(nome, idade, matricula)
            self.alunos[matricula] = novo_aluno
            print(f"Aluno {nome} cadastrado com sucesso.")
        else:
            print(f"Matrícula {matricula} já cadastrada para outro aluno.")

    def buscar_aluno(self, matricula):
        if matricula in self.alunos:
            return self.alunos[matricula]
        else:
            print(f"Aluno com matrícula {matricula} não encontrado.")
            return None


# Exemplo de uso do sistema
sistema = SistemaCadastro()

# Cadastro de alunos
sistema.cadastrar_aluno("Lekler", 21, "12345")
sistema.cadastrar_aluno("Alexandre Rodrigues", 22, "67890")

# Matricular alunos em matérias
aluno_lekler = sistema.buscar_aluno("12345")
if aluno_lekler:
    aluno_lekler.matricular_materia("Microeconomia")
    aluno_lekler.matricular_materia("Macroeconomia")
    aluno_lekler.matricular_materia("Econometria")
    aluno_lekler.matricular_materia("Finanças Públicas")
    aluno_lekler.matricular_materia("História do Pensamento Econômico")

aluno_alexandre = sistema.buscar_aluno("67890")
if aluno_alexandre:
    aluno_alexandre.matricular_materia("Estatística")
    aluno_alexandre.matricular_materia("Projeto de Ciência de Dados 1")

# Adicionar notas
if aluno_lekler:
    aluno_lekler.adicionar_nota("Microeconomia", 8.5)
    aluno_lekler.adicionar_nota("Macroeconomia", 7.5)
    aluno_lekler.adicionar_nota("Econometria", 9.0)
    aluno_lekler.adicionar_nota("Finanças Públicas", 8.0)
    aluno_lekler.adicionar_nota("História do Pensamento Econômico", 7.8)

if aluno_alexandre:
    aluno_alexandre.adicionar_nota("Estatística", 9.2)
    aluno_alexandre.adicionar_nota("Projeto de Ciência de Dados 1", 8.9)

# Exibir boletim
if aluno_lekler:
    aluno_lekler.exibir_boletim()

if aluno_alexandre:
    aluno_alexandre.exibir_boletim()

# Exibir informações completas do aluno
if aluno_lekler:
    aluno_lekler.exibir_informacoes()

if aluno_alexandre:
    aluno_alexandre.exibir_informacoes()
