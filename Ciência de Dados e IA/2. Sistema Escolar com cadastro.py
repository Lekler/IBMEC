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

# Função principal para interagir com o usuário


def main():
    sistema = SistemaCadastro()

    while True:
        print("\nSistema de Cadastro de Alunos")
        print("1. Cadastrar Aluno")
        print("2. Matricular Aluno em Matéria")
        print("3. Adicionar Nota")
        print("4. Exibir Boletim")
        print("5. Exibir Informações Completas do Aluno")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do aluno: ")
            idade = int(input("Idade do aluno: "))
            matricula = input("Matrícula do aluno: ")
            sistema.cadastrar_aluno(nome, idade, matricula)

        elif opcao == "2":
            matricula = input("Matrícula do aluno: ")
            aluno = sistema.buscar_aluno(matricula)
            if aluno:
                materia = input("Nome da matéria: ")
                aluno.matricular_materia(materia)

        elif opcao == "3":
            matricula = input("Matrícula do aluno: ")
            aluno = sistema.buscar_aluno(matricula)
            if aluno:
                materia = input("Nome da matéria: ")
                nota = float(input("Nota: "))
                aluno.adicionar_nota(materia, nota)

        elif opcao == "4":
            matricula = input("Matrícula do aluno: ")
            aluno = sistema.buscar_aluno(matricula)
            if aluno:
                aluno.exibir_boletim()

        elif opcao == "5":
            matricula = input("Matrícula do aluno: ")
            aluno = sistema.buscar_aluno(matricula)
            if aluno:
                aluno.exibir_informacoes()

        elif opcao == "6":
            print("Encerrando o sistema.")
            break

        else:
            print("Opção inválida, tente novamente.")


# Executar a função principal
if __name__ == "__main__":
    main()
