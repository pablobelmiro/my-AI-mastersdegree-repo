# Conversor de Autômatos: NFA-ε → NFA → DFA

Este projeto foi desenvolvido como parte do **Laboratório 01** da disciplina de **Teoria da Computação** (Mestrado). O objetivo é implementar a conversão formal de Autômatos Finitos Não-Determinísticos com transições vazias (NFA-ε) para Autômatos Finitos Determinísticos (DFA).

## Como Executar

### Pré-requisitos
- GHC (Haskell Compiler)
- Biblioteca `yaml` do Haskell

### Usando o Nix (Recomendado)
```bash
nix-shell
# Dentro do shell, execute:
runghc Main-2-1-conversao-automatos.hs nfae.yaml
```

### Execução Direta
```bash
runghc Main-2-1-conversao-automatos.hs nfae.yaml
```

## Estrutura do Projeto

- `Main-2-1-conversao-automatos.hs`: Código fonte principal em Haskell.
- `nfae.yaml`: Arquivo de entrada com a definição do NFA-ε.
- `dfa.yaml`: Arquivo de saída gerado com o DFA equivalente.
- `shell.nix`: Configuração do ambiente para reprodutibilidade.
- `explicacao_conversor.md`: Relatório técnico detalhando a lógica acadêmica.

## Lógica Implementada

O conversor segue um pipeline de duas etapas:
1.  **Remoção de Epsilon:** Transforma o NFA-ε em um NFA simples através do cálculo de Epsilon-Closure.
2.  **Construção de Subconjuntos:** Transforma o NFA em um DFA através da união de estados alcançáveis.

---
**Aluno:** Pablo Belmiro
**Referência:** Michael Sipser - Introdução à Teoria da Computação.
**Professor:** 
