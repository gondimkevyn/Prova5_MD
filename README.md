# Problema 5: Divisão Inteira por Subtração Sucessiva
**Disciplina:** Matemática Discreta  
**Professor:** Edjard Mota

---

## 👥 Integrantes da Equipe
* **Cassia Sousa Ataide** - Matrícula: `22450505`
* **Felipe Alves de Oliveira** - Matrícula: `22554310`
* **Kevyn do Nascimento Paz Gondim** - Matrícula: `22153920`
* **Lucas Henry Garcia Freire** - Matrícula: `22554313`
* **Pollyanna da Silva Brelaz** - Matrícula: `22350982`

---

## 1. Contextualização e Especificação Formal

Antes da implementação da lógica, o comportamento do algoritmo é mapeado no domínio lógico-matemático através de contratos formais que definem as propriedades de corretude:

* **Pré-condição ($P$):** O dividendo ($a$) deve ser um inteiro não-negativo e o divisor ($b$) deve ser estritamente maior que zero ($a \geq 0 \land b > 0$).
* **Pós-condição ($Q$):** Ao término da execução, o quociente calculado ($q$) e o resto ($r$) devem corresponder exatamente às propriedades da divisão euclidiana ($q = a \div b \land r = a \pmod b$).
* **Invariante de Loop ($I$):** A relação aritmética fundamental da divisão deve se manter verdadeira antes e depois de cada iteração do laço, garantindo que o dividendo original seja igual ao quociente atual vezes o divisor, somado ao resto corrente ($a_{orig} = q \cdot b + r \land r \geq 0$).
* **Função Variante ($V$):** Definida pelo valor corrente do resto ($V(\text{state}) = r$). Ela atua como uma métrica de progresso delimitada inferiormente por $0$, decrescendo estritamente a cada iteração para provar matematicamente a terminação do laço.

---

## 2. Análise Teórica do Bug de Terminação (Código Original)

A implementação inicial fornecida para o exercício apresenta uma falha crítica na manipulação das variáveis de estado dentro do laço de repetição:

* **O Bug:** No corpo do loop, o algoritmo incrementa corretamente o contador do quociente, porém omite completamente a operação de subtração sucessiva no dividendo.
* **Consequência:** Como o valor do dividendo nunca é reduzido, a guarda do laço permanece indefinidamente verdadeira se a entrada inicial satisfizer a condição de entrada. Isso resulta em um travamento por laço infinito (divergência).

---

## 3. Estrutura de Instrumentação Formal do Algoritmo

Para transformar o código em um programa verificado em tempo de execução, aplicamos sistematicamente as diretrizes do roteiro utilizando a primitiva `assert` do Python, dividida em 5 etapas obrigatórias:

1. **1. ASSERCAO DE PRE-CONDICAO:** Injetada no início da função para validar se os parâmetros fornecidos pertencem ao domínio aceito pelo algoritmo antes de iniciar qualquer cálculo.
2. **2. ASSERCAO DE INICIALIZACAO (CASO BASE):** Posicionada imediatamente antes da entrada do laço `while`. Avalia se as atribuições iniciais das variáveis de estado satisfazem o Invariante de Loop.
3. **3. ASSERCAO DE MANUTENCAO (PASSO INDUTIVO):** Localizada ao final do corpo do laço, logo após a atualização das variáveis de controle. Comprova que a propriedade do invariante se preserva da iteração $k$ para a iteração $k + 1$.
4. **4. ASSERCAO DE DECREMENTO (PROGRESSO DA TERMINACAO):** Avalia se o valor da Função Variante após o passo é estritamente menor do que o valor capturado no início da iteração, garantindo convergência em direção ao limite inferior.
5. **5. ASSERCAO DE POS-CONDICAO (DEDUCAO FINAL):** Posicionada logo após a saída do bloco do laço e antes do retorno do programa. Valida se o estado final deduzido corresponde perfeitamente à especificação matemática alvo do problema.

---

## 4. Execução e Análise Dinâmica de Falha 

Ao submeter a versão incorreta ao ambiente instrumentado, o ecossistema de verificação reage impedindo o comportamento indefinido:

* **Qual Asserção Estoura:** A asserção responsável por validar o progresso do laço (**4. ASSERÇÃO DE DECREMENTO**) dispara imediatamente, levantando uma exceção de interrupção (`AssertionError`).
* **Razão Aritmética:** Para que a terminação de um loop seja provada sobre o conjunto bem-ordenado dos números naturais N{0, 1, ...}, a função variante $V(\text{state})$ = a deve decrescer estritamente a cada iteração ($V_{k+1} < V_k$). Como a subtração foi omitida no código bugado, o estado mantém-se fixo ($V_{k+1} = V_k$). Frente a uma guarda que exige que o dividendo seja maior ou igual ao divisor, o progresso métrico colapsa, disparando o alarme da asserção antes que o programa trave a máquina em um loop infinito.

---

## 5. Cenários Práticos para Testar e Estourar Cada Asserção

O sistema de checagem em tempo de execução pode ser testado induzindo falhas controladas através dos seguintes cenários e dados de entrada:

### 1. Disparo da Asserção de Pré-condição
* **Dataset Usado:** `a = 10, b = 0` (ou qualquer dividendo negativo como `a = -5, b = 3`).
* **Como Induzir:** Fornecer dados que quebrem as restrições iniciais da divisão. O próprio contrato bloqueia a execução no primeiro passo.

### 2. Disparo da Asserção de Inicialização (Caso Base)
* **Dataset Usado:** `a = 10, b = 3`
* **Como Induzir:** Alterar propositalmente o valor inicial da variável do resto logo na atribuição (ex: definir `r = a + 1` antes do loop). O verificador detecta que o caso base não bate com o dividendo original e interrompe a execução.

### 3. Disparo da Asserção de Manutenção (Passo Indutivo)
* **Dataset Usado:** `a = 10, b = 3`
* **Como Induzir:** Forçar um erro matemático na atualização do quociente dentro do loop (ex: modificar o incremento para somar de dois em dois, `y = y + 2`). O assert de manutenção detecta o desequilíbrio na equação do invariante ao final da primeira iteração.

### 4. Disparo da Asserção de Decremento (Função Variante)
* **Dataset Usado:** `a = 10, b = 3` (ou `a = 5, b = 5`)
* **Como Induzir:** Cenário idêntico ao bug original. Comentar a linha responsável por subtrair o divisor do resto corrente. O verificador identifica a ausência de progresso métrico e barra a execução infinita.

### 5. Disparo da Asserção de Pós-condição (Dedução Final)
* **Dataset Usado:** `a = 10, b = 3`
* **Como Induzir:** Alterar o valor acumulado das variáveis de saída logo após o encerramento do laço `while`, mas antes do retorno (ex: inserir a linha `y = y - 1`). O loop executa e termina normalmente, mas a validação final detecta que a resposta entregue não condiz com a especificação real.
