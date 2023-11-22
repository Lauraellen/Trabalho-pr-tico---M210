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
    variaveis_restricao = []
    for i in range(num_restricoes):
        expressao = []

        for j in range(len(variaveis)):
            coeficiente = float(input(f"Digite o coeficiente para a variável {variaveis[j]} na restrição {i + 1}: "))
            expressao.append(coeficiente)

        sinal = input(f"Digite o sinal de desigualdade (<= ou >=) para a restrição {i + 1}: ")
        valor = float(input(f"Digite o valor para a restrição {i + 1}: "))
        restricao_nome = input(f"Digite o nome para a restrição {i + 1}: ")

        variaveis_restricao.append(restricao_nome);
        # Adiciona os coeficientes, sinal e valor à lista da restrição
        expressao.extend([sinal, valor])

        # Adiciona a lista da restrição à lista de restrições
        restricoes.append(expressao)

    return restricoes, variaveis_restricao


# Exemplo de uso
variaveis_decisao = addVariablesDecision()
funcao_objetivo_resultante, coeficientes = createFunction(variaveis_decisao)
restricoes_resultantes, restricoes_nome = getRestricts(variaveis_decisao)
variaveisAuxiliares = []
quadros = []
print(restricoes_nome)
def getGreatValues():
    funcao_objetivo = [-coeficiente for coeficiente in coeficientes]
    funcao_objetivo.append(0)
    restricoes_na_forma_canonica = [converter_restricoes_para_forma_canonica(restricao) for restricao in restricoes_resultantes]

    gerar_novo_quadro({}, funcao_objetivo, restricoes_na_forma_canonica)
    return obter_valores_otimos();


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


def calcular_valores_nova_linha(quadro_antigo, indice_linha, indice_coluna_pivo, indice_linha_pivo):
    valor_elemento_pivo = quadro_antigo["valores"][indice_linha_pivo][indice_coluna_pivo]
    linha_referencia = [valor / valor_elemento_pivo for valor in quadro_antigo["valores"][indice_linha_pivo]]
    new_linha = []

    if indice_linha == indice_linha_pivo:
        new_linha = linha_referencia
    else:
        new_linha = [valor + (-1 * quadro_antigo["valores"][indice_linha][indice_coluna_pivo] * linha_referencia[index])
                     for index, valor in enumerate(quadro_antigo["valores"][indice_linha])]

    return new_linha

def obter_valores_otimos():
    quadro_novo = quadros[-1]
    continuar_iteracao = verificar_se_ainda_ha_elementos_negativos(quadro_novo)

    if not continuar_iteracao:
        return obter_valores_otimos_pelo_quadro(quadro_novo)
    elif len(quadros) == 100:
        quadro_com_maior_lucro = None
        maior_lucro = 0

        for quadro in quadros:
            if quadro["valores"][0][-1] > maior_lucro:
                maior_lucro = quadro["valores"][0][-1]
                quadro_com_maior_lucro = quadro

        return obter_valores_otimos_pelo_quadro(quadro_com_maior_lucro)
    else:
        elemento_pivo = obter_elemento_pivo(quadro_novo)
        gerar_novo_quadro(elemento_pivo)
        return obter_valores_otimos()

def verificar_se_ainda_ha_elementos_negativos(quadro):
    return any(elemento < 0 for elemento in quadro["valores"][0])

def obter_valores_otimos_pelo_quadro(ultimo_quadro):
    valores_otimos = []

    for variavel in variaveis_decisao:
        index_valor_otimo_variavel = ultimo_quadro["linhas"].index(variavel) if variavel in ultimo_quadro["linhas"] else -1

        if index_valor_otimo_variavel != -1:
            valor_otimo_variavel = ultimo_quadro["valores"][index_valor_otimo_variavel][-1]
            valores_otimos.append({
                "variavel": variavel,
                "valor_otimo": valor_otimo_variavel
            })
        else:
            valores_otimos.append({
                "variavel": variavel,
                "valor_otimo": 0
            })

    return valores_otimos

def obter_elemento_pivo(quadro):
    indice_coluna_pivo = quadro["valores"][0].index(min(quadro["valores"][0]))
    relacao_ld_com_a_coluna_pivo = []
    for restricao in quadro["valores"]:
        valor = restricao[-1] / restricao[indice_coluna_pivo] \
            if restricao[indice_coluna_pivo] > 0 else float('inf')
        relacao_ld_com_a_coluna_pivo.append(valor)

    menor_valor = min(relacao_ld_com_a_coluna_pivo)
    indice_linha_pivo = relacao_ld_com_a_coluna_pivo.index(menor_valor)

    return {"indiceColunaPivo": indice_coluna_pivo, "indiceLinhaPivo": indice_linha_pivo}

def gerar_novo_quadro(elemento_pivo, funcao_objetivo=None, restricoes_na_forma_canonica=None):


    if not quadros:
        num_variaveis_auxiliares = len(variaveisAuxiliares)

        quadros.append({
            "valores": [funcao_objetivo]
        })

        quadros[0]["colunas"] = variaveis_decisao + variaveisAuxiliares
        quadros[0]["linhas"] = ["Z"] + variaveisAuxiliares

        for _ in range(num_variaveis_auxiliares):
            quadros[0]["valores"][0].append(0)

        for index, restricao in enumerate(restricoes_na_forma_canonica):
            quadros[0]["valores"].append(restricao.copy())

            if index == 0:
                for _ in range(num_variaveis_auxiliares - 1):
                    quadros[0]["valores"][-1].insert(-1, 0)
            else:
                for i in range(index):
                    quadros[0]["valores"][-1].insert(-2, 0)

                for _ in range(num_variaveis_auxiliares - index - 1):
                    quadros[0]["valores"][-1].insert(-1, 0)
    else:
        ultima_posicao = len(quadros)
        new_quadro = {
            "colunas": quadros[ultima_posicao - 1]["colunas"][:],
            "linhas": quadros[ultima_posicao - 1]["linhas"][:],
            "valores": [linha[:] for linha in quadros[ultima_posicao - 1]["valores"]]  # Cria cópias das listas internas
        }

        new_quadro["colunas"][elemento_pivo["indiceColunaPivo"]] = quadros[ultima_posicao - 1]["linhas"][
            elemento_pivo["indiceLinhaPivo"]]
        new_quadro["linhas"][elemento_pivo["indiceLinhaPivo"]] = quadros[ultima_posicao - 1]["colunas"][
            elemento_pivo["indiceColunaPivo"]]

        for index, linha in enumerate(new_quadro["valores"]):
            new_quadro["valores"][index] = calcular_valores_nova_linha(quadros[ultima_posicao - 1], index,
                                                                       elemento_pivo["indiceColunaPivo"],
                                                                       elemento_pivo["indiceLinhaPivo"])

        quadros.append(new_quadro)

valores_otimo = getGreatValues()
print('VALORES OTIMOS => ', valores_otimo)

def obter_lucro_total(valores_otimos):
    lucro_total = 0
    for indice in valores_otimos:
        indice_variavel = variaveis_decisao.index(indice["variavel"])
        lucro_total += coeficientes[indice_variavel] * indice["valor_otimo"]
    return lucro_total

lucro_total = obter_lucro_total(valores_otimo)
print('Lucro total => ', lucro_total)

def obter_preco_sombra():
    # valores_otimos = gerar_valores_otimos(variaveis_input, coeficientes_fo_input, restricoes_input)
    ultimo_quadro = quadros[-1]
    precos_sombra = []
    for index, valor in enumerate(ultimo_quadro["valores"][0]):

        if ultimo_quadro["colunas"][index-1] and index >= (len(ultimo_quadro["valores"][0]) - len(variaveisAuxiliares) - 1):
            precos_sombra.append({
                "variavel": ultimo_quadro["colunas"][index-1],
                "precoSombra": valor
            })


    for i, preco_sombra in enumerate(precos_sombra):
        if(i < len(restricoes_nome)):
            precos_sombra[i]["variavel"] = restricoes_nome[i]

    return precos_sombra

preco_sombra = obter_preco_sombra()
#ajustar retorno do preço sombra
print('Preço sombra => ', preco_sombra)