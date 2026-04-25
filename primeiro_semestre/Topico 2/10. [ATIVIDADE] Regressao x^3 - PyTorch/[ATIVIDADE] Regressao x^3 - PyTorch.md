Atividade Prática – Regressão com Redes Neurais

Forma de envio: O envio deve ser feito exclusivamente pelo Moodle, por meio do upload do notebook preenchido. O(a) aluno(a) deve inserir seu nome no arquivo e responder a todas as seções solicitadas.
Objetivo da Atividade

O objetivo desta atividade é aplicar os conceitos estudados sobre regressão com redes neurais artificiais, utilizando o PyTorch para modelar dados que seguem um padrão cúbico. A tarefa envolve tanto o diagnóstico do comportamento de modelos quanto a modificação prática da arquitetura de redes neurais para alcançar melhor desempenho.
Estrutura da Tarefa

A atividade está dividida em três questões principais:
Questão 1 – Diagnóstico do modelo

    O(a) aluno(a) deverá analisar o gráfico de predição do modelo sobre os dados de treino e teste.

    A análise deve identificar se o modelo apresenta underfitting, overfitting ou ajuste adequado (good fit).

    A justificativa deve considerar:

        A forma da curva ajustada (suave, oscilante, aderente aos dados).

        Diferenças de desempenho entre treino e teste.

        Evidências de ruído ou desvios sistemáticos.

Questão 2 – Ajuste da rede neural

    Alterar a estrutura da rede para que ela consiga se ajustar corretamente à curva dos dados, definida por:
    y=x3+ruıˊdo
    y=x3+ruıˊdo

    O código inicial dado possui uma rede muito simples.

    O(a) aluno(a) deve:

        Modificar a quantidade de neurônios em cada camada.

        Se necessário, adicionar mais camadas ocultas.

        Testar diferentes arquiteturas até obter um ajuste satisfatório.

    O critério de sucesso é que a curva predita acompanhe corretamente o comportamento cúbico dos dados.

Questão 3 – Ajuste do número de épocas

    Após obter uma rede com complexidade adequada, o(a) aluno(a) deverá reduzir o número de épocas de treinamento.

    O objetivo é encontrar o menor valor possível que ainda permita boa convergência.

    Passos a seguir:

        Diminuir progressivamente o número de épocas (ex.: de 1000 para 500, 200 ou menos).

        Executar novamente o treinamento.

        Verificar o gráfico da função de perda (loss) para avaliar convergência.

        Analisar se o desempenho permanece satisfatório.

    O(a) aluno(a) deve responder:

        Qual foi o menor número de épocas utilizado que manteve bom desempenho?

        Como avaliou que esse valor foi suficiente?
