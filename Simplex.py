def addVariablesDecision():

    num_variaveis = int(input("Quantas variáveis de decisão você deseja inserir? "))

    variaveis = []

    for i in range(num_variaveis):
        nome_variavel = input(f"Digite o nome da variável de decisão {i + 1}: ")
        variaveis.append(nome_variavel)

    return variaveis

def createFunction(variaveis):
    coeficientes = []
    for variavel in variaveis:
        coeficiente = float(input(f"Digite o coeficiente para a variável {variavel}: "))
        coeficientes.append(coeficiente)

    funcao_objetivo = "Z = "
    for i in range(len(variaveis)):
        funcao_objetivo += f"{coeficientes[i]} * {variaveis[i]}"
        if i < len(variaveis) - 1:
            funcao_objetivo += " + "

    return funcao_objetivo

def getRestricts(variaveis):
    num_restricoes = int(input("Quantas restrições você deseja adicionar? "))

    restricoes = []

    for i in range(num_restricoes):
        expressao = ""
        for j in range(len(variaveis)):
            coeficiente = float(input(f"Digite o coeficiente para a variável {variaveis[j]} na restrição {i + 1}: "))
            expressao += f"{coeficiente} * {variaveis[j]}"

            if j < len(variaveis) - 1:
                expressao += " + "

        sinal = input(f"Digite o sinal de desigualdade (<= ou >=) para a restrição {i + 1}: ")
        valor = float(input(f"Digite o valor para a restrição {i + 1}: "))
        expressao += f" {sinal} {valor}"

        restricoes.append(expressao)

    return restricoes

# Exemplo de uso
variaveis_decisao = addVariablesDecision()
funcao_objetivo_resultante = createFunction(variaveis_decisao)
print("Função objetivo resultante:", funcao_objetivo_resultante)

restricoes_resultantes = getRestricts(variaveis_decisao)

print("Restrições resultantes:")
for restricao in restricoes_resultantes:
    print(restricao)



