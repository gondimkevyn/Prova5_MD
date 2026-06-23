def multiplica_por_somas(a: int, b: int) -> int:
    # Pre-condicao: os dois numeros tem que ser nao-negativos,
    # senao a ideia de "somar a, b vezes" nem faz sentido
    assert a >= 0 and b >= 0, "a e b precisam ser >= 0"

    resultado = 0
    somas_feitas = 0  # quantas vezes "a" ja foi somado até agora

    # Antes do loop comecar, nenhuma soma foi feita ainda, entao resultado
    # tem que ser igual a a * 0 = 0. Se isso nao for verdade, algo
    # ja comecou errado antes mesmo do loop rodar.
    assert resultado == a * somas_feitas, "ja comecou errado: resultado deveria ser 0"

    while somas_feitas < b:
        # quanto ainda falta ser somado (isso so pode diminuir, nunca
        # aumentar, senao o loop nunca acaba)
        faltam_somar = b - somas_feitas
        assert faltam_somar >= 0, "nao pode faltar um numero negativo de somas"

        # AQUI ESTA O BUG: era pra ser somado "a", mas por descuido foi somado "b"
        resultado = resultado + b
        somas_feitas += 1

        # depois de cada soma, o resultado tem que bater com a * somas_feitas
        # essa e a parte que vai estourar primeiro
        assert resultado == a * somas_feitas, (
            f"deu errado na soma numero {somas_feitas}: "
            f"resultado ficou {resultado}, mas devia ser {a * somas_feitas}"
        )

        # confirma que houve avanco real (faltam_somar diminuiu)
        assert (b - somas_feitas) < faltam_somar, "o loop nao esta avancando"

    # no final, resultado tem que ser exatamente a vezes b
    assert resultado == a * b, "resultado final nao corresponde a a * b"

    return resultado


if __name__ == "__main__":
    a, b = 5, 3
    print(f"Calculando {a} x {b} somando {a} repetidamente, {b} vezes...")
    print(multiplica_por_somas(a, b))