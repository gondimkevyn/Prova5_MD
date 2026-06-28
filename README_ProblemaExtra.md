
# Problema Extra: Multiplicação Inteira por Somas Sucessivas

**Multiplicação Inteira por Somas Sucessivas**

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

### Limitação Detectada no Conjunto de Asserções

A análise formal do invariante e do passo indutivo revela uma lacuna na capacidade de detecção do bug pelo assert de manutenção:

**O bug só é detectado quando o laço executa pelo menos uma vez (`b > 0`) e `a ≠ b`.**

A justificativa decorre diretamente da avaliação do invariante na primeira iteração:

- Se `b = 0`, a guarda do `while` (`somas_feitas < b`) é falsa desde o início. O laço não executa, e nenhuma asserção do corpo é avaliada. O programa retorna `0`, satisfazendo a pós-condição trivialmente, mesmo com a linha errada presente.
- Se `b > 0` e `a = b`, a linha bugada `resultado = resultado + b` produz, numericamente, o mesmo efeito que a linha correta `resultado = resultado + a`. Consequentemente, o invariante `resultado = a × somas_feitas` é mantido em todas as iterações, e o programa termina sem disparar nenhum assert.
- Se `b > 0` e `a ≠ b`, a primeira iteração gera `resultado = b`, enquanto o invariante exige `resultado = a × 1 = a`. Como `a ≠ b`, a asserção de manutenção é violada e o bug é exposto.

**Prova algébrica:** na primeira iteração, `resultado_novo = 0 + b = b`. O assert de manutenção exige `resultado_novo == a * 1`, ou seja, `b == a`. Essa igualdade só é verdadeira quando `a = b`. Logo, a detecção ocorre **se, e somente se**, `b > 0` e `a ≠ b`.

**Implicação prática:** o dataset fornecido (`a=5, b=3`) é adequado para expor o bug porque satisfaz a condição de detecção. Entretanto, a suíte de asserções não constitui uma prova geral de corretude, uma vez que sua eficácia depende da escolha dos valores de teste. Para `b=0` ou `a=b`, o programa passa por todas as asserções sem erro, mascarando a falha semântica.

**Recomendação:** a suíte de testes deve obrigatoriamente incluir ao menos um caso com `b > 0` e `a ≠ b` para que a asserção de manutenção exerça seu papel de detector do bug. Casos com `b = 0` ou `a = b` são válidos para verificar os limites da especificação, mas não são suficientes para expor este erro específico.

### Correção

Basta trocar a linha `resultado = resultado + b` por `resultado = resultado + a`. Com essa correção, o algoritmo passa por todas as 5 asserções até a pós-condição, para o Data Set e quaisquer outros valores válidos de `a` e `b`.
