# Roadmap – Reconhecimento de Padrões
**Professor:** Francisco de Assis Boldt

Roadmap do conteúdo teórico e prático abordado na disciplina, cobrindo desde os fundamentos de Aprendizado de Máquina até Redes Neurais.

---

## 1. Introdução

- **Aprendizado de Máquina e Reconhecimento de Padrões**: origem histórica de termos como IA, Redes Neurais, Mineração de Dados e Big Data, e como o Aprendizado de Máquina se diferencia do desenvolvimento tradicional de software.
- **Tipos de Aprendizado de Máquina**: classificação por classe de problema (supervisionado, não supervisionado, por reforço), por forma de treinamento (batch ou online) e por tipo de generalização (por instância ou por modelo).
- **Ambiente para estudar Aprendizado de Máquina**: opções de ambiente (Google Colab, Anaconda, Python local), criação de ambiente virtual com `venv`, e instalação de bibliotecas como Jupyter, NumPy, Pandas, SciPy e scikit-learn.

## 2. Regressão

- **Fontes de dados para treinar modelos**: repositórios como UCI Machine Learning Repository, Kaggle, AWS Open Data, além de meta-portais e páginas agregadoras de datasets.
- **Análise do dataset Boston Housing**: carregamento, visualização e aplicação de um modelo linear com `sklearn.datasets`.
- **Métricas de desempenho para regressão**: Erro Absoluto Médio (MAE), Erro Quadrático Médio (MSE) e Raiz do Erro Quadrático Médio (RMSE).
- **Implementação intuitiva de um modelo de aprendizado**: construção de um algoritmo iterativo de regressão linear a partir da intuição.
- **Vetorização do algoritmo de aprendizado**: reescrita do algoritmo de regressão linear com notação vetorial para atualização iterativa dos pesos.
- **Análise da função de erro**: estudo gráfico do comportamento do MSE durante o treinamento iterativo.
- **Uso da classe `LinearRegression` do scikit-learn**: aplicação com uma única característica e depois com todas as características da base.

## 3. Classificação

- **Classificação binária**: adaptação de um estimador de regressão linear para o problema de classificação binária, usando a base de câncer de mama (`load_breast_cancer`).
- **Visualização da função de erro na classificação**: diferenças em relação ao comportamento suave da função de erro da regressão.
- **Classificação multiclasse**: exemplos onde cada instância pertence a exatamente uma entre várias classes.
- **Classificação multirrótulo**: exemplo construído a partir da base `load_digits`, utilizando o classificador `KNeighborsClassifier`.

## 4. Generalização

- **Conceito de generalização**: generalização por instância com o algoritmo do vizinho mais próximo e importância da separação treino/teste.
- **Divisão treino e teste**: necessidade de embaralhar os dados antes de dividir a base.
- **Validação aninhada**: separação em treino, validação e teste para escolha correta de hiperparâmetros.
- **Pipelines**: importância de aplicar qualquer tratamento de dados ou ajuste de estimadores somente após a divisão treino/teste.
- **Ajuste automático de hiperparâmetros**: riscos de viés quando o ajuste é feito manualmente pelo programador com acesso à base de teste.
- **`GridSearchCV`**: uso para busca automática de hiperparâmetros, mitigando o risco de viés.
- **`GridSearchCV` combinado com `Pipeline`**: estratégias de combinação (`GridSearchCV(Pipeline)` ou `Pipeline(GridSearchCV)`) conforme a necessidade de desempenho.

## 5. Árvores de Decisão

- **Implementação intuitiva para atributos discretos**: conceitos de classificador ZeroR, impureza Gini e cálculo de impureza por nó, com abordagem recursiva de força bruta.
- **Visualização de regiões de decisão**: construção de função para exibir graficamente as regiões de decisão de um classificador em 2D.
- **Heurística gulosa para atributos contínuos**: busca dos melhores limiares de corte para cada característica.
- **Treinamento com atributos contínuos e categóricos**: aplicação prática usando o dataset Titanic (Kaggle).

## 6. Ensembles

- **Combinação de estimadores**: conceito de ensemble como combinação de modelos divergentes para melhorar o desempenho preditivo.

## 7. Aprendizado Não Supervisionado

- **Implementação simplificada do KMeans**: algoritmo de agrupamento simples e eficiente para dados não rotulados.
- **Aprendizado semi-supervisionado**: uso combinado de dados rotulados e não rotulados.
- **Redução de dimensionalidade**: técnicas para reduzir o número de características mantendo a informação relevante.

## 8. Redes Neurais Lineares

- **O Perceptron**: implementação em Python do modelo de rede neural proposto em 1958.
- **Perceptron com Hinge Loss**: efeito da troca da função de custo na atualização dos pesos e no hiperplano separador resultante.
- **Perceptron e Adaline**: comparação de comportamento usando a regra delta de Widrow-Hoff.
- **Neurônio de Bias**: motivo de sua necessidade e por que nem sempre aparece explicitamente nos diagramas de redes neurais.
- **Taxa de aprendizado e descida de gradiente**: impacto da taxa de aprendizado na convergência ou divergência do treinamento.
- **Perceptron Multiclasse**: estratégia semelhante à abordagem "um contra todos".
- **Pseudo Inversa para treinar classificadores lineares**: uso da pseudo inversa como alternativa à descida de gradiente para calcular os pesos.

## 9. Redes Neurais com Camada Oculta

- **Extreme Learning Machine**: arquitetura simples capaz de lidar com problemas não linearmente separáveis.
- **Backpropagation simplificado**: implementação para uma arquitetura de camada oculta única com dois neurônios.
- **Backpropagation com múltiplas camadas**: extensão da implementação anterior para arquiteturas multicamadas (MLP).

---

*Roadmap baseado no conteúdo do curso "Reconhecimento de Padrões", ministrado por Francisco de Assis Boldt (Ifes/Cefor). Tarefas, apresentações e questionários avaliativos não foram incluídos, conforme solicitado.*
