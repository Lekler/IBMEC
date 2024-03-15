#15/03/23

#1-Decomposição
#2- Reconhecendo padrões
   #2.1- Recursão
    #2.2- Fatorial (n!)
    #2.3- Fatorial sem recursão
n = 4
if n == 0:
    resultado = 1 
else:
    resultado = 1
    for i in range(1, n + 1): 
        resultado *= i

#3- Chamando a função fatorial recursiva
def fatorial(n):
    if n==0:
        return 1
    else:
        return n*fatorial(n-1)

n = 5
resultado = fatorial(n)
print(f'O fatorial de {n} é {resultado}')

#4- Gerando a sequência de Fibonacci
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_seq = [0, 1]
        for i in range(2, n):
            fib_seq.append(fib_seq[i-1] + fib_seq[i-2])
        return fib_seq

n = 10
fibonacci_seq = fibonacci(n)
print(f"A sequência de Fibonacci com {n} elementos é: {fibonacci_seq}")



numbers = []
for _ in range(20):
    number = int(input("Digite um número inteiro: "))
    numbers.append(number)

max_value = max(numbers)
min_value = min(numbers)

print(f"O maior valor fornecido é: {max_value}")
print(f"O menor valor fornecido é: {min_value}")