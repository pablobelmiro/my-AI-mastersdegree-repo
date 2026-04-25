# Relatório Técnico: Implementação Modular NFA-$\epsilon$ \rightarrow$ NFA $\rightarrow$ DFA

Este documento detalha a implementação do conversor de autômatos desenvolvido em Haskell, estruturado para atender aos requisitos do **Laboratório 01**. A principal evolução desta versão é a separação clara entre a remoção de transições vazias e a construção de subconjuntos.

---

## 1. Fundamentação Teórica: Pipeline de Conversão

Para atingir o determinismo partindo de um NFA-$\epsilon$, seguimos um fluxo modular que garante a correção teórica e a clareza algorítmica:

1.  **Etapa 1 ($NFA\text{-}\epsilon \rightarrow NFA$):** Eliminação das transições $\epsilon$ e recalculação dos estados de aceitação.
2.  **Etapa 2 ($NFA \rightarrow DFA$):** Aplicação da Construção de Subconjuntos sobre o autômato já simplificado.

---

## 2. Etapa 1: Remoção de Transições Vazias (`removerEpsilon`)

Nesta fase, o objetivo é criar um autômato equivalente que não dependa de saltos espontâneos. 

### A Lógica Algorítmica
Para cada estado $s$ e cada símbolo do alfabeto $\sigma$, calculamos o novo destino através da composição:
$$\delta'(s, \sigma) = E(\delta(E(s), \sigma))$$
Onde $E(s)$ representa o **Fecho-Epsilon** (todos os estados alcançáveis via $\epsilon$ a partir de $s$).

### Critério de Aceitação
Um estado no novo NFA torna-se final se o seu próprio fecho-$\epsilon$ contiver pelo menos um estado final do autômato original. Isso garante que a capacidade de aceitação por caminhos vazios seja preservada.

---

## 3. Etapa 2: Construção de Subconjuntos (`construcaoSubconjuntos`)

Com um NFA sem transições $\epsilon$, aplicamos o algoritmo de **Subset Construction**.

### Estados Coletivos
Cada estado no DFA é uma representação de um conjunto de estados do NFA. Na implementação, esses estados são nomeados através da junção dos IDs originais por vírgulas (ex: `"1,3"`).

### Exploração Dinâmica (`resolver`)
Utilizamos uma busca recursiva que:
- Parte do estado inicial.
- Descobre novos destinos para cada símbolo do alfabeto.
- Adiciona apenas destinos inéditos à fila de pendentes, garantindo que o algoritmo pare (convergência).

---

## 4. Análise da Estrutura do Código Haskell

A implementação prioriza a legibilidade acadêmica através de nomes de funções intuitivos:

- **`pegarFecho`**: Implementa a recursão de ponto fixo para encontrar o limite do alcance $\epsilon$.
- **`buscarDestinos`**: Uma abstração simples para filtrar transições no YAML.
- **`resolver`**: O motor de busca em largura que mapeia o espaço de estados do DFA.

No `main`, o fluxo reflete exatamente o pedido no laboratório:
```haskell
-- Passo 1: NFA-epsilon -> NFA
let nfa = removerEpsilon nfae
-- Passo 2: NFA -> DFA
let dfa = construcaoSubconjuntos nfa
```

---

## 5. Conclusão e Nuances do Mestrado

Para um aluno de mestrado, esta abordagem modular demonstra uma compreensão superior da **composição de algoritmos**. Em vez de tratar a conversão como uma "caixa preta", o código prova que cada transformação é uma operação independente sobre o modelo formal do autômato, facilitando a verificação de corretude em cada estágio.

**Valores Gerados:**
- **Iniciais:** O estado inicial do DFA é o conjunto `{initial_state}` do NFA limpo.
- **Finais:** Aplicamos o critério de interseção ($R \cap F_{NFA} \neq \emptyset$) para definir os estados de aceitação do DFA.

---
**Keywords:** Modularidade, Haskell, Epsilon-Removal, Subset Construction, Sipser N4.
