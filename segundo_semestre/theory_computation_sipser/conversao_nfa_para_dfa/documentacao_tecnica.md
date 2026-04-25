# Documentação Técnica: Do Formalismo de Sipser à Implementação em Haskell

Este documento oferece uma imersão técnica no código fonte do conversor de autômatos, correlacionando as definições formais de Michael Sipser com as estruturas e a sintaxe da linguagem Haskell.

---

## 1. Fundamentos Teóricos (Sipser)

De acordo com Sipser, um autômato é uma 5-tupla $(Q, \Sigma, \delta, q_0, F)$. A conversão implementada ataca dois desafios distintos do não-determinismo:

### 1.1. O Desafio do Epsilon ($\epsilon$)
A transição vazia introduz o conceito de **Fecho-Epsilon** ($E(R)$). Para qualquer conjunto de estados $R \subseteq Q$, $E(R)$ é o conjunto de estados alcançáveis a partir de $R$ seguindo apenas transições $\epsilon$.
- **Na prática:** O código implementa isso como um cálculo de *ponto fixo* na função `pegarFecho`.

### 1.2. A Construção de Subconjuntos
Para converter um NFA em DFA, cada estado do DFA deve corresponder a um elemento do **Conjunto das Partes** de $Q$, ou seja, $\mathcal{P}(Q)$.
- **Regra de Transição:** Para um estado do DFA $R$ e símbolo $a$:
  $\delta'(R, a) = \{q \in Q \mid q \in E(\delta(r, a)) \text{ para algum } r \in R\}$

---

## 2. Anatomia do Código Haskell

Haskell foi escolhida por sua proximidade matemática, permitindo que a implementação espelhe as definições de conjuntos quase literalmente.

### 2.1. Estruturas de Dados e Tipagem
Utilizamos **Records** para definir o `Automato`. A sintaxe `data` cria novos tipos, e a derivação `Generic` (obtida via Pragma no topo do arquivo) permite a ponte com o formato YAML.
```haskell
data Automato = Automato {
    type_         :: String, -- Tipo do autômato (nfae, dfa)
    alphabet      :: [String], -- Alfabeto Σ
    states        :: [String], -- Conjunto Q
    -- ... demais campos
}
```

### 2.2. Pattern Matching e List Comprehension
A função `buscarDestinos` utiliza **Pattern Matching** nos argumentos e uma **List Comprehension** (compreensão de lista) para filtrar as transições:
```haskell
buscarDestinos estadoProcurado simboloProcurado listaTotal =
    [ t_to | Transicao t_from t_sym t_to <- listaTotal, t_from == estadoProcurado, t_sym == simboloProcurado ]
```
*   `Transicao t_from t_sym t_to`: Desestrutura o objeto diretamente no loop.
*   Isso é semanticamente equivalente a dizer: $\{to \mid (from, sym, to) \in Transitions, from = q, sym = a\}$.

### 2.3. Recursão e Imutabilidade
Diferente de linguagens imperativas com loops `while`, o motor de busca do DFA (`resolver`) utiliza **Recursão de Cauda**:
```haskell
resolver vistos (atual:resto) transAcumuladas
```
- `(atual:resto)`: É o padrão de desestruturação de listas em Haskell (*head* e *tail*).
- **Imutabilidade:** Não alteramos listas existentes. Em cada passo recursivo, passamos uma "nova versão" do acumulador e da lista de vistos.

---

## 3. Fluxo de Transformação Modular

A implementação segue um pipeline em duas etapas, respeitando a separação de preocupações:

### Etapa A: `removerEpsilon`
Esta função atua como um pré-processador. Ela "achata" o autômato, embutindo as transições $\epsilon$ nas transições de símbolos reais.
- **Nuance:** Um estado se torna final se ele consegue "enxergar" um estado final original através de uma névoa de transições $\epsilon$.

### Etapa B: `construcaoSubconjuntos`
Aqui ocorre a explosão (ou expansão) de estados.
- **Gestão de Nomes:** Usamos `intercalate ","` para converter a lista de estados do NFA (ex: `["1", "3"]`) no nome do estado do DFA (ex: `"1,3"`).
- **Ordenação:** O uso de `sort` é vital para garantir que o conjunto $\{1, 3\}$ não seja tratado como diferente de $\{3, 1\}$, evitando estados duplicados no DFA.

---

## 4. Por que Haskell para Teoria da Computação?

1.  **Pureza:** Funções matemáticas puras não têm efeitos colaterais, facilitando a prova de que a conversão está correta.
2.  **Expressividade:** A capacidade de tratar funções como cidadãos de primeira classe permite que operações de conjuntos sejam escritas de forma compacta.
3.  **Segurança:** O sistema de tipos garante que você não tente transitar para um estado que não existe ou use um símbolo fora do alfabeto definido.

---
**Conclusão Técnica:** A implementação mapeia a teoria de Sipser transformando a busca não-determinística em uma árvore de busca determinística sobre o espaço de subconjuntos, garantindo que o DFA resultante aceite exatamente a mesma linguagem que o NFA-$\epsilon$ original.
