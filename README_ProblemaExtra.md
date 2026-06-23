
# Problema Extra: Multiplicação Inteira por Somas Sucessivas

Multiplicacao Inteira por Somas Sucessivas
Ideia: multiplicar a por b somando "a" repetidamente, b vezes.
Ex: 5 x 3 = 5 + 5 + 5 = 15

Aqui foi deixado propositalmente um erro no codigo (pra fins do exercicio)
e tudo foi instrumentado com asserts pra provar, passo a passo, onde o
algoritmo quebra a logica esperada.

## Especificação Lógico-Matemática

- **Pré-condição:** `a ≥ 0`, `b ≥ 0`
- **Pós-condição:** `resultado = a × b`
- **Invariante de Loop:** `resultado = a × somas_feitas` (onde `somas_feitas` é quantas vezes já somamos `a`)
- **Função Variante:** `V(state) = b - somas_feitas` (número de somas que ainda faltam; começa em `b` e deve chegar a 0)

## Descrição

O algoritmo calcula `a × b` somando o valor de `a` exatamente `b` vezes, usando um laço `while`.

## Data Set

| a | b | resultado esperado |
|---|---|---------------------|
| 5 | 3 | 15                  |

## O Bug Semântico Proposital

No corpo do loop, em vez de acumular `resultado = resultado + a`, o código soma `resultado = resultado + b` por engano.

## Código Instrumentado

Ver `mult_sucessiva.py`. Segue as 5 etapas do roteiro:
1. Asserção de Pré-condição — `a >= 0 and b >= 0`
2. Asserção de Inicialização (Caso Base) — `resultado == a * somas_feitas` com `somas_feitas = 0`
3. Asserção de Manutenção (Passo Indutivo) — `resultado == a * somas_feitas` após cada iteração
4. Asserção de Progresso e Limite — captura `faltam_somar = b - somas_feitas`, garante `>= 0` e que `(b - somas_feitas) < faltam_somar` depois do passo
5. Asserção de Pós-condição — `resultado == a * b`

## Execução e Análise de Falha

Ao executar o algoritmo com o Data Set fornecido (`a = 5`, `b = 3`), o programa abortou a execução e levantou um `AssertionError` na **Asserção de Manutenção (Passo 3)**, dentro do laço `while`, logo na primeira iteração.

Saída real obtida no terminal:

```
Calculando 5 x 3 somando 5 repetidamente, 3 vezes...
Traceback (most recent call last):
  File "mult_sucessiva.py", line 54, in <module>
    print(multiplica_por_somas(a, b))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "mult_sucessiva.py", line 37, in multiplica_por_somas
    assert resultado == a * somas_feitas, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: deu errado na soma numero 1: resultado ficou 3, mas devia ser 5
```

### Razão Aritmética do Bug

A especificação exige que o invariante `resultado = a × somas_feitas` se mantenha verdadeiro após cada iteração. Na primeira iteração (`somas_feitas` passa de `0` para `1`):

- O código bugado executa `resultado = resultado + b`, ou seja, `resultado = 0 + 3 = 3`.
- O assert avalia `resultado == a * somas_feitas` → `3 == 5 * 1` → `3 == 5` → **Falso**.

Como o lado esquerdo (`resultado = 3`) não corresponde ao lado direito (`a × somas_feitas = 5`), o invariante de manutenção foi violado, quebrando a prova de correção por indução do algoritmo: a propriedade que deveria se preservar de uma iteração para a próxima (`k` → `k+1`) não se sustenta.

### Correção

Basta trocar a linha `resultado = resultado + b` por `resultado = resultado + a`. Com essa correção, o algoritmo passa por todas as 5 asserções até a pós-condição, para o Data Set e quaisquer outros valores válidos de `a` e `b`.