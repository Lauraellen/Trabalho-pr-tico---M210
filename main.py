variaveis = []
coeficientesFO = []
restricoes = []
variaveisAuxiliares = []
quadros = []
restricoesNaFormaCanonica = []
funcaoObjetivo = []

def gerarValoresOtimos(variaveisInput, coeficientesFOInput, restricoesInput):
    instanciarVariaveis(variaveisInput, coeficientesFOInput, restricoesInput)
    global funcaoObjetivo
    funcaoObjetivo = [-coeficiente for coeficiente in coeficientesFO] + [0]
    global restricoesNaFormaCanonica
    restricoesNaFormaCanonica = [converterRestricoesParaFormaCanonica(restricao) for restricao in restricoes]
    gerarNovoQuadro()  # primeiro quadro
    return obterValoresOtimos()

def instanciarVariaveis(variaveisInput, coeficientesFOInput, restricoesInput):
    global variaveis, coeficientesFO, restricoes, variaveisAuxiliares, quadros
    variaveis = variaveisInput
    coeficientesFO = coeficientesFOInput
    restricoes = restricoesInput
    variaveisAuxiliares = []
    quadros = []

def converterRestricoesParaFormaCanonica(restricao):
    restricaoNaFormaCanonica = restricao.copy()
    simboloDeDesigualdade = restricao[-2]
    proxVariavelAuxiliar = (
        variaveisAuxiliares[-1][:-1] + str(variaveisAuxiliares.index[-1] + 2)
        if variaveisAuxiliares
        else "aux1"
    )
    variaveisAuxiliares.append(proxVariavelAuxiliar)

    if simboloDeDesigualdade == "≤":
        restricaoNaFormaCanonica[-2] = 1
    elif simboloDeDesigualdade == "≥":
        restricaoNaFormaCanonica[-2] = -1

    return restricaoNaFormaCanonica

def gerarNovoQuadro(elementoPivo=None):
    global quadros
    if not quadros:
        numVariaveisAuxiliares = len(variaveisAuxiliares)

        quadros.append(
            {"valores": [funcaoObjetivo]}
        )

        quadros[0]["colunas"] = variaveis + variaveisAuxiliares
        quadros[0]["linhas"] = ["Z"] + variaveisAuxiliares

        for _ in range(numVariaveisAuxiliares):
            quadros[0]["valores"][0].append(0)

        for index, restricao in enumerate(restricoesNaFormaCanonica):
            quadros[0]["valores"].append(restricao.copy())

            if index == 0:
                for _ in range(numVariaveisAuxiliares - 1):
                    indiceAdicionar = len(restricao) - 1
                    quadros[0]["valores"][-1].insert(indiceAdicionar, 0)
            else:
                for i in range(index):
                    indiceAdicionar = len(restricao) - 2
                    quadros[0]["valores"][-1].insert(indiceAdicionar, 0)

                for i in range(numVariaveisAuxiliares - index - 1):
                    indiceAdicionar = len(restricao)
                    quadros[0]["valores"][-1].insert(indiceAdicionar, 0)
    else:
        ultimaPosicao = len(quadros)
        newQuadro = quadros[ultimaPosicao - 1].copy()
        newQuadro["colunas"][elementoPivo["indiceColunaPivo"]] = quadros[
            ultimaPosicao - 1
        ]["linhas"][elementoPivo["indiceLinhaPivo"]]
        newQuadro["linhas"][elementoPivo["indiceLinhaPivo"]] = quadros[
            ultimaPosicao - 1
        ]["colunas"][elementoPivo["indiceColunaPivo"]]
        for index, linha in enumerate(newQuadro["valores"]):
            newQuadro["valores"][index] = calcularValoresNovaLinha(
                quadros[ultimaPosicao - 1],
                index,
                elementoPivo["indiceColunaPivo"],
                elementoPivo["indiceLinhaPivo"],
            )
        quadros.append(newQuadro)

def obterValoresOtimos():
    quadroNovo = quadros[-1]
    continuarIteracao = verificarSeAindaHaElementosNegativos(quadroNovo)
    if not continuarIteracao:
        return obterValoresOtimosPeloQuadro(quadroNovo)
    elif len(quadros) == 100:
        quadroComMaiorLucro = max(
            quadros, key=lambda q: q["valores"][0][-1]
        )
        return obterValoresOtimosPeloQuadro(quadroComMaiorLucro)
    else:
        gerarNovoQuadro(obterElementoPivo(quadroNovo))
        return obterValoresOtimos()

def obterValoresOtimosPeloQuadro(ultimoQuadro):
    valoresOtimos = []
    for variavel in variaveis:
        indexValorOtimoVariavel = ultimoQuadro["linhas"].index(variavel) if variavel in ultimoQuadro["linhas"] else -1
        if indexValorOtimoVariavel != -1:
            valorOtimoVariavel = ultimoQuadro["valores"][indexValorOtimoVariavel][-1]
            valoresOtimos.append(
                {"variavel": variavel, "valorOtimo": valorOtimoVariavel}
            )
        else:
            valoresOtimos.append({"variavel": variavel, "valorOtimo": 0})
    return valoresOtimos

def obterLucroTotal(valoresOtimos):
    lucroTotal = 0
    for indice in valoresOtimos:
        indiceVariavel = variaveis.index(indice["variavel"])
        lucroTotal += coeficientesFO[indiceVariavel] * indice["valorOtimo"]
    return lucroTotal

def obterPrecoSombra(variaveisInput, coeficientesFOInput, restricoesInput, variaveisDasRestricoesInput):
    valoresOtimos = gerarValoresOtimos(
        variaveisInput, coeficientesFOInput, restricoesInput
    )
    ultimoQuadro = quadros[-1]

    precosSombra = [
        {"variavel": ultimoQuadro["colunas"][index], "precoSombra": valor}
        for index, valor in enumerate(ultimoQuadro["valores"][0])
        if ultimoQuadro["colunas"][index]
        and index >= (len(ultimoQuadro["valores"][0]) - len(variaveisAuxiliares) - 1)
    ]

    for i, precoSombra in enumerate(precosSombra):
        precoSombra["variavel"] = variaveisDasRestricoesInput[i]

    return precosSombra

def verificarViabilidadeENovoLucro(
    variaveisInput, coeficientesFOInput, restricoesInput, variacoesDeDisponibilidadeInput
):
    valoresOtimos = gerarValoresOtimos(
        variaveisInput, coeficientesFOInput, restricoesInput
    )
    ultimoQuadro = quadros[-1]

    viavel = verificarViabilidade(ultimoQuadro, variacoesDeDisponibilidadeInput)

    if not viavel:
        return False

    novoLucro = 0
    for index, valor in enumerate(ultimoQuadro["valores"][0]):
        if index >= (len(ultimoQuadro["valores"][0]) - len(variacoesDeDisponibilidadeInput) - 1):
            if index < (len(ultimoQuadro["valores"][0]) - 1):
                novoLucro += (
                    variacoesDeDisponibilidadeInput[
                        index
                        - (
                            len(ultimoQuadro["valores"][0])
                            - len(variacoesDeDisponibilidadeInput)
                            - 1
                        )
                    ]
                    * valor
                )
    return novoLucro

def calcularValoresNovaLinha(quadroAntigo, indiceLinha, indiceColunaPivo, indiceLinhaPivo):
    valorElementoPivo = quadroAntigo["valores"][indiceLinhaPivo][indiceColunaPivo]
    linhaReferencia = [
        valor / valorElementoPivo for valor in quadroAntigo["valores"][indiceLinhaPivo]
    ]
    if indiceLinha == indiceLinhaPivo:
        newLinha = linhaReferencia
    else:
        newLinha = [
            valor
            + (-1 * quadroAntigo["valores"][indiceLinha][indiceColunaPivo] * referencia)
            for valor, referencia in zip(
                quadroAntigo["valores"][indiceLinha], linhaReferencia
            )
        ]

    return newLinha


def obterElementoPivo(quadro):
    indiceColunaPivo = quadro["valores"][0].index(min(quadro["valores"][0]))
    relacaoDoLDComAColunaPivo = [
        restricao[indiceColunaPivo] > 0 and restricao[-1] / restricao[indiceColunaPivo]
        or float("inf")
        for restricao in quadro["valores"][1:]
    ]
    menorValor = min(relacaoDoLDComAColunaPivo)
    indiceLinhaPivo = relacaoDoLDComAColunaPivo.index(menorValor) + 1
    return {"indiceColunaPivo": indiceColunaPivo, "indiceLinhaPivo": indiceLinhaPivo}


def verificarSeAindaHaElementosNegativos(quadro):
    return any(elemento < 0 for elemento in quadro["valores"][0])


def verificarViabilidade(ultimoQuadro, variacoesDeDisponibilidade):
    for indice, valor in enumerate(ultimoQuadro["valores"]):
        if indice != 0:
            valorSoma = 0
            for i, v in enumerate(valor):
                if i >= (len(valor) - len(variacoesDeDisponibilidade) - 1):
                    if i == (len(valor) - 1):
                        valorSoma += v
                    else:
                        valorSoma += (
                            variacoesDeDisponibilidade[
                                i - (len(valor) - len(variacoesDeDisponibilidade) - 1)
                            ]
                            * v
                        )
            if valorSoma < 0:
                return False
    return True
