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

    return funcao_objetivo, coeficientes

def getRestricts(variaveis):
    num_restricoes = int(input("Quantas restrições você deseja adicionar? "))

    restricoes = []

    for i in range(num_restricoes):
        expressao = []
        for j in range(len(variaveis)):
            coeficiente = float(input(f"Digite o coeficiente para a variável {variaveis[j]} na restrição {i + 1}: "))
            expressao.append(coeficiente)

        sinal = input(f"Digite o sinal de desigualdade (<= ou >=) para a restrição {i + 1}: ")
        valor = float(input(f"Digite o valor para a restrição {i + 1}: "))

        # Adiciona os coeficientes, sinal e valor à lista da restrição
        expressao.extend([sinal, valor])

        # Adiciona a lista da restrição à lista de restrições
        restricoes.append(expressao)

    return restricoes


# Exemplo de uso
variaveis_decisao = addVariablesDecision()
funcao_objetivo_resultante, coeficientes = createFunction(variaveis_decisao)
restricoes_resultantes = getRestricts(variaveis_decisao)
variaveisAuxiliares = []

def getGreatValues():
    print(variaveis_decisao)
    print(funcao_objetivo_resultante)
    print(coeficientes)
    print(restricoes_resultantes)

    funcao_objetivo = [-coeficiente for coeficiente in coeficientes]
    funcao_objetivo.append(0)
    restricoes_na_forma_canonica = [converter_restricoes_para_forma_canonica(restricao) for restricao in restricoes_resultantes]
    print(restricoes_na_forma_canonica)
    print(funcao_objetivo)



def converter_restricoes_para_forma_canonica(restricao):
    restricao_na_forma_canonica = restricao.copy()
    simbolo_de_desigualdade = restricao[-2]
    prox_variavel_auxiliar = variaveisAuxiliares[-1][: -1] + str(len(variaveisAuxiliares) + 1) if len(
        variaveisAuxiliares) > 0 else "aux1"
    variaveisAuxiliares.append(prox_variavel_auxiliar)

    if simbolo_de_desigualdade == "<=":
        restricao_na_forma_canonica[-2] = 1
    elif simbolo_de_desigualdade == ">=":
        restricao_na_forma_canonica[-2] = -1

    return restricao_na_forma_canonica


getGreatValues()

