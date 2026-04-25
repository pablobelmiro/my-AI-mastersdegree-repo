# Parte 2: Motor de Expressões Regulares

Este diretório contém a implementação do motor de reconhecimento de Expressões Regulares baseado na **Construção de Thompson**.

## 🛠️ Como Executar

Dentro do ambiente `nix-shell`, você pode rodar o motor passando a regex e a palavra:

```bash
# Exemplo 1: União
runghc Main-3-regular-expression.hs "(P|p)ablo" Pablo

# Exemplo 2: Repetições
runghc Main-3-regular-expression.hs "ab*" abbbbb
```

Caso queira apenas gerar o arquivo YAML do autômato:
```bash
runghc Main-3-regular-expression.hs "a+b?"
```

## 📜 Sintaxe Suportada

- `ab` : Concatenação
- `a|b` : União
- `a*` : Fecho de Kleene (zero ou mais)
- `a+` : Uma ou mais repetições
- `a?` : Opcional (zero ou uma)
- `( )` : Agrupamento

## 📂 Arquivos

- `Main-3-regular-expression.hs`: Lógica principal (Parser + Thompson + Simulador).
- `explicacao_regex.md`: Relatório técnico detalhado com diagramas e exemplos de teste.
- `shell.nix`: Ambiente de execução reproduzível.
