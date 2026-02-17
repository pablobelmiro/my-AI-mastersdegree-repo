#################### NEWWWWWWWWW ####################
#################### FUNÇÕES PLOTAGEM GRÁFICO SIMULATED ANNEALING ####################
from IPython.display import clear_output
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_path(cities_xy, cities_path, ax):

    # Reeordena as cidades pela ordem do caminho
    cities = cities_xy[cities_path]

    # Repete a primeira cidade para fechar o ciclo
    x = cities[:,0]
    y = cities[:,1]

    # Personalização do gráfico
    ax.set_xlabel('X (Longitude)')
    ax.set_ylabel('Y (Latitude)')
    ax.set_title('Caminho')

    # Plotagem das coordenadas interligadas com pontos vermelhos e linhas azuis
    ax.plot(x, y, color='blue', linestyle='-', linewidth=2)
    ax.plot(x, y, color='red', marker='o', markersize=8, linestyle='')
    ax.plot(x[[-1,0]], y[[-1,0]], color='orange', linestyle='-', linewidth=2)

def plot_distances(iteration_list, distance_list, best_distances, ax):

    x  = iteration_list
    y1 = distance_list
    y2 = best_distances

    # Personalização do gráfico
    ax.set_xlabel('Iterações')
    ax.set_ylabel('Distâncias (custos)')
    ax.set_title('Comprimento Total do caminho')

    ax.plot(x,y1, label='Atual')
    ax.plot(x,y2, label='Melhor')
    ax.legend()

def plot_acceptance_prob(iteration_list, accept_p_list, ax):

    x = iteration_list
    y = accept_p_list

    # Personalização do gráfico
    ax.set_xlabel('Iterações')
    ax.set_ylabel('Probabilidade')
    ax.set_title('Probabilidade de Aceitação')

    ax.set_ylim([0, 1.05])

    # Criar uma nova lista de cores com base nos valores de y
    xc, yc, colors = zip(*[(xi, yi, 'b') if yi==1.0 else (xi, yi, 'r') \
                           for xi, yi in enumerate(y)])

    ax.scatter(xc, yc, c=colors, s=2)

def plot_temperature(iteration_list, temperat_list, ax):

    x = iteration_list
    y = temperat_list

    # Personalização do gráfico
    ax.set_xlabel('Iterações')
    ax.set_ylabel('Temperatura')
    ax.set_title('Decaimento da Temperatura')

    ax.set_ylim([0, 1000])

    ax.plot(x,y)

def plot_axes_figure(cities_xy, cities_path, iteration_list,
                     distance_list, best_distances,
                     accept_p_list, temperat_list):

    x = iteration_list
    y1 = distance_list
    y2 = best_distances
    y3 = accept_p_list
    y4 = temperat_list

    clear_output(wait=True)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12,8))

    plot_path(cities_xy, cities_path, ax1)
    plot_distances      (x, y1, y2, ax2)
    plot_acceptance_prob(x, y3, ax3)
    plot_temperature    (x, y4, ax4)

    # Ajusta o espaçamento entre os subgráficos
    fig.tight_layout()

    plt.pause(0.001)

def boxplot_sorted(df, rot=90, figsize=(12,6), fontsize=20, algoritmo=""):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    
    # Prepara o DataFrame transposto para cálculo das medianas
    df2 = df.T
    meds = df2.median(axis=1).sort_values(ascending=False)
    
    # Gera o boxplot ordenado
    axes = df.reindex(columns=meds.index).boxplot(figsize=figsize, rot=rot, fontsize=fontsize,
        boxprops=dict(linewidth=4, color='cornflowerblue'),
        whiskerprops=dict(linewidth=4, color='cornflowerblue'),
        medianprops=dict(linewidth=4, color='firebrick'),
        capprops=dict(linewidth=4, color='cornflowerblue'),
        flierprops=dict(marker='o', markerfacecolor='dimgray',
            markersize=12, markeredgecolor='black'),
        return_type="axes")

    # Adiciona títulos e rótulos
    title = f"Boxplot algoritmo {algoritmo}"
    axes.set_title(title, fontsize=fontsize + 5)
    axes.set_ylabel("Distância (Custo)", fontsize=fontsize)
    axes.set_xlabel("Configurações / Algoritmos", fontsize=fontsize)
    
    # Calcula e adiciona resumo estatístico como texto no gráfico
    stats_text = "Resumo Estatístico:\n"
    for col in meds.index:
        col_data = df[col].dropna()
        stats_text += f"\n[{col}]\n"
        stats_text += f" Méd: {col_data.mean():.1f}\n"
        stats_text += f" Mediana: {col_data.median():.1f}\n"
        stats_text += f" Std: {col_data.std():.1f}\n"
        stats_text += f" Q1 (25%): {col_data.quantile(0.25):.1f}\n"
        stats_text += f" Q3 (75%): {col_data.quantile(0.75):.1f}\n"
        stats_text += f" Mín: {col_data.min():.1f}\n"
        stats_text += f" Máx: {col_data.max():.1f}"
    
    # Posiciona a caixa de texto
    axes.text(1.02, 0.5, stats_text, transform=axes.transAxes, 
              verticalalignment='center', fontsize=fontsize - 10,
              bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    
    axes.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

def plota_rotas(df_cidades, ordem_cidades, algoritmo=""):
    if not isinstance(df_cidades, pd.DataFrame):
        df_cidades = pd.DataFrame(df_cidades, columns=['X', 'Y'])
    
    df_solucao = df_cidades.copy()
    df_solucao = df_solucao.iloc[ordem_cidades]

    X = df_solucao['X']
    Y = df_solucao['Y']
    cidades = list(df_solucao.index)
    ordem_visita = list(range(1, len(X) + 1))

    # cria objeto gráfico
    fig = go.Figure()

    # gera linhas e marcadores com gradiente de cor para a sequência
    fig.add_trace(go.Scatter(
        x=X, y=Y,
        text=cidades,
        customdata=ordem_visita,
        mode='lines+markers',
        marker=dict(
            size=10,
            color=ordem_visita,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Ordem de Visita'),
            line=dict(width=1, color='DarkSlateGrey')
        ),
        line=dict(width=2, color='royalblue'),
        hovertemplate='<b>Cidade: %{text}</b><br>Ordem na Rota: %{customdata}<br>X: %{x}<br>Y: %{y}<extra></extra>',
        name='Trajeto'
    ))

    # Destaque para o Ponto de Partida
    fig.add_trace(go.Scatter(
        x=[X.iloc[0]], y=[Y.iloc[0]],
        mode='markers',
        marker=dict(size=14, color='gold', symbol='diamond', line=dict(width=2, color='black')),
        name='Início',
        hoverinfo='skip'
    ))

    # acrescenta linha tracejada para fechar o ciclo (retorno ao início)
    fig.add_trace(go.Scatter(
        x=X.iloc[[-1,0]], y=Y.iloc[[-1,0]],
        mode='lines',
        line=dict(dash='dash', color='firebrick', width=2),
        name='Fechamento do Ciclo',
        hovertext='Retorno ao ponto inicial',
        hoverinfo='text'
    ))

    title = f'Visualização Interativa da Rota (TSP) aplicada ao algoritmo {algoritmo}'
    fig.update_layout(
        title=title,
        xaxis_title='X (Longitude)',
        yaxis_title='Y (Latitude)',
        template='plotly_white',
        width=800, height=600,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig.show()

#################### SIMULATED ANNEALING ####################
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ----- calculo da distancia euclidiana
def calculate_distance(city_a, city_b):
    dx = city_a[0] - city_b[0]
    dy = city_a[1] - city_b[1]
    dist = math.sqrt(dx**2 + dy**2)
    return dist

# ----- calcula a distância total de um caminho completo.
def total_distance(route, distance_matrix):
    total = 0
    for i in range(len(route) - 1):
        city_a = route[i]
        city_b = route[i + 1]
        total += distance_matrix[city_a, city_b]

    total += distance_matrix[route[-1], route[0]]

    return total

def generate_neighbor(route):
    new_route = route.copy()
    n = len(new_route)

    index_a = random.randint(0, n-1)
    index_b = random.randint(0, n-1)

    new_route[index_a], new_route[index_b] = new_route[index_b], new_route[index_a]
    return new_route

def acceptance_probability(current_distance, new_distance, temperature):
    if new_distance < current_distance: # melhor == menor (<)
        return 1.0
    else:
        delta = (current_distance - new_distance)

        return math.exp(delta / temperature)

def generate_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i, j] = calculate_distance(cities[i], cities[j])

    return distance_matrix, num_cities

"""
cities: Uma lista ou array com as coordenadas (x, y) de todas as cidades.
initial_temperature: A temperatura inicial do sistema.
cooling_rate: A taxa na qual a temperatura diminui.
iterations: O número total de 'passos' do algoritmo.
nrep=50: Número de repetition (ou vizinhos testados) para cada iteração principal de resfriamento.
"""
def simulated_annealing(cities, initial_temperature, cooling_rate, iterations, nrep=50):

    num_cities = len(cities)

    distance_matrix, num_cities = generate_distance_matrix(cities)

    current_route = np.arange(num_cities)
    best_route = current_route.copy()

    current_distance = total_distance(current_route, distance_matrix)
    best_distance = current_distance

    temperature = initial_temperature

    iteration_list = []
    best_distances = []
    distance_list  = []
    accept_p_list  = []
    temperat_list  = []

    for iteration in range(iterations):
        # numero de vizinhos a serem gerados e testados para cada iteração
        for _ in range(nrep):
            new_route = generate_neighbor(current_route)
            new_distance = total_distance(new_route, distance_matrix)

            acceptance_prob = acceptance_probability(current_distance, new_distance, temperature)

            if random.random() < acceptance_prob:
                current_route = new_route
                current_distance = new_distance

        temperature *= cooling_rate

        if new_distance < best_distance:
            best_route = new_route
            best_distance = new_distance

        iteration_list += [iteration]
        best_distances += [best_distance]
        distance_list  += [current_distance]
        accept_p_list  += [acceptance_prob]
        temperat_list  += [temperature]

        # if iteration % 50 == 0:
        #     plot_axes_figure(cities, current_route, iteration_list,
        #                     distance_list, best_distances,
        #                     accept_p_list, temperat_list)

    plt.show()
    return best_route, best_distance


#---------- Get TSP dataset
def get_tsp_data(dataset_name):
    url = f'http://www.math.uwaterloo.ca/tsp/world/{dataset_name}.tsp'
    
    try:
        df = pd.read_table(
            url,
            skiprows=7,
            names=['ID', 'X', 'Y'], 
            sep=' ',
            skipinitialspace=True,
            index_col=0,
            skipfooter=1,
            engine='python'
        )
        return df[['X', 'Y']].values
        
    except Exception as e:
        try:
             df = pd.read_table(
                url,
                skiprows=7, 
                names=['ID', 'X', 'Y'],
                sep=r'\s+',
                index_col=0,
                skipfooter=1,
                engine='python'
            )
             return df[['X', 'Y']].values
        except Exception as e2:
            print(f"Erro ao ler dados de {url}: {e} // {e2}")
            return None


def run_simulated_annealing(dataset_name):
    """Execução do SA com parâmetros escalonados pelo número de cidades."""
    cities = get_tsp_data(dataset_name)
    num_cities = len(cities)
    
    # Parâmetros adaptativos para comparação justa
    total_calls = num_cities * 15000
    iterations = num_cities * 500
    nrep = 20 #total_calls // iterations
    
    print(f"Iniciando SA para {dataset_name}: {num_cities} cidades, Iters={iterations}, Nrep={nrep}...")
    best_route, best_distance = simulated_annealing(cities, 
                                                    initial_temperature=1000.0, 
                                                    cooling_rate=0.9997, 
                                                    iterations=iterations,
                                                    nrep=nrep)

    print("SA Best distance:", best_distance)
    return best_route, best_distance

#################### EXECUÇÃO SIMULATED ANNEALING ####################
datasets = ['wi29']
    
print("Iniciando processamento em lote...")
best_route_tsp_sa = []
best_distance_tsp_sa = []
for ds in datasets:
    try:
       best_route_tsp_sa, best_distance_tsp_sa = run_simulated_annealing(dataset_name=ds)
    except Exception as e:
        print(f"Erro crítico ao processar {ds}: {e}")

#################### MELHOR ROTA SIMULATED ANNEALING ####################
print("Melhor caminho:")
plota_rotas(get_tsp_data('wi29'), best_route_tsp_sa, "Simulated Annealing")
print("\n")

#################### BOXPLOT SIMULATED ANNEALING ####################
print("boxplot_sorted:")
boxplot_sorted(df=best_route_tsp_sa, algoritmo="Simulated Annealing")
print("\n")

#################### TABELA SIMULATED ANNEALING ####################
print("Representação do Estado (Figura 4):")
df_estado = pd.DataFrame([best_route_tsp_sa])
print(df_estado.to_string(index=False, header=False))

print("\nTabela com dados SA (Resumo dos Trechos):")
# Utiliza a rota atual para calcular estatísticas dos segmentos (trechos)
cities_xy = get_tsp_data(datasets[0])
dists_sa = [np.linalg.norm(cities_xy[best_route_tsp_sa[i]] - cities_xy[best_route_tsp_sa[(i+1)%len(best_route_tsp_sa)]]) for i in range(len(best_route_tsp_sa))]
df_custo = pd.DataFrame({'Simulated Annealing (Segmentos)': dists_sa})
print(df_custo.describe().rename(index={'mean': 'Méd', '50%': 'Mediana', 'std': 'Std', '25%': 'Q1 (25%)', '75%': 'Q3 (75%)', 'min': 'Mín', 'max': 'Máx'}))
print("\n")


#################### NEWWWWW ####################
#################### FUNÇÕES PLOTAGEM GRÁFICO GENETIC ALGORITHM ####################
def plot_ga_path(cities_xy, cities_path, ax):
    ax.clear()
    # Insere a cidade 0 no início para fechar o ciclo
    full_path = np.insert(cities_path, 0, 0)
    cities = cities_xy[full_path]
    x, y = cities[:,0], cities[:,1]
    ax.set_title('Melhor Caminho GA (Ciclo Completo)')
    ax.plot(x, y, color='green', linestyle='-', linewidth=2)
    ax.plot(x, y, color='red', marker='o', markersize=6, linestyle='')
    ax.plot(x[[-1,0]], y[[-1,0]], color='orange', linestyle='-', linewidth=2)

def plot_ga_convergence(best_fitness_history, ax):
    ax.clear()
    ax.set_title('Convergência (Best Fitness)')
    ax.set_xlabel('Gerações')
    ax.set_ylabel('Fitness')
    ax.plot(best_fitness_history, color='tab:blue', linewidth=2)
    if len(best_fitness_history) > 0:
        ax.text(0.95, 0.95, f'Melhor: {best_fitness_history[-1]:.2f}', 
                transform=ax.transAxes, horizontalalignment='right', 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    ax.grid(True, linestyle='--', alpha=0.6)

def plot_ga_diversity(std_fitness_history, ax):
    ax.clear()
    ax.set_title('Diversidade Genética (Std Dev)')
    ax.set_xlabel('Gerações')
    ax.set_ylabel('Std Dev')
    ax.plot(std_fitness_history, color='tab:purple', linewidth=1.5)
    ax.fill_between(range(len(std_fitness_history)), std_fitness_history, color='tab:purple', alpha=0.2)
    if len(std_fitness_history) > 0:
        ax.text(0.95, 0.95, f'Std: {std_fitness_history[-1]:.2f}', 
                transform=ax.transAxes, horizontalalignment='right', 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    ax.grid(True, linestyle='--', alpha=0.6)

def plot_ga_landscape(current_aptidoes, ax):
    ax.clear()
    ax.set_title('Paisagem de Aptidão (Geração Atual)')
    ax.set_xlabel('Indivíduos')
    ax.set_ylabel('Fitness')
    
    # Criar escala de cores baseada no fitness
    sc = ax.scatter(range(len(current_aptidoes)), current_aptidoes, 
                    c=current_aptidoes, cmap='viridis_r', s=15, alpha=0.7, label='Indivíduos')
    
    # Linha de média
    mean_val = np.mean(current_aptidoes)
    ax.axhline(mean_val, color='tab:red', linestyle='--', alpha=0.5, label=f'Média: {mean_val:.1f}')
    
    # Destacar o melhor destaque
    best_idx = np.argmin(current_aptidoes)
    ax.scatter(best_idx, current_aptidoes[best_idx], color='gold', marker='*', s=150, 
               edgecolors='black', label='Melhor', zorder=5)
    
    ax.legend(fontsize='x-small', loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)

def plot_ga_figure(cities_xy, best_route, best_fitness_history, std_fitness_history, current_aptidoes):
    fig, axes = plt.subplots(2, 2, figsize=(12,8))
    (ax1, ax2), (ax3, ax4) = axes
    plot_ga_path(cities_xy, best_route, ax1)
    plot_ga_convergence(best_fitness_history, ax2)
    plot_ga_diversity(std_fitness_history, ax3)
    plot_ga_landscape(current_aptidoes, ax4)
    fig.tight_layout()
    plt.show()

#################### GENETIC ALGORITHM ####################
def gera_individuo(num_cities):
    """Gera um indivíduo aleatório (permutação das cidades exceto a 0)."""
    return np.random.permutation(np.arange(1, num_cities))

def gera_populacao_inicial(num_cities, tam_pop):
    """Gera a população inicial com indivíduos aleatórios."""
    populacao = [gera_individuo(num_cities) for _ in range(tam_pop)]
    return populacao

def fitness(individuo, distance_matrix):
    """Calcula a aptidão reinserindo a cidade 0 no início do trajeto."""
    full_route = np.insert(individuo, 0, 0)
    return total_distance(full_route, distance_matrix)

def crossover_ox(pai1, pai2):
    """Order 1 Crossover (OX) para manter a validade da permutação."""
    n = len(pai1)
    filho = [-1] * n
    
    # Seleciona um segmento do pai1
    start, end = sorted(random.sample(range(n), 2))
    filho[start:end+1] = pai1[start:end+1]
    
    # Preenche o resto com o pai2
    p2_idx = (end + 1) % n
    f_idx = (end + 1) % n
    
    genes_no_filho = set(filho)
    
    while -1 in filho:
        gene = pai2[p2_idx]
        if gene not in genes_no_filho:
            filho[f_idx] = gene
            genes_no_filho.add(gene)
            f_idx = (f_idx + 1) % n
        p2_idx = (p2_idx + 1) % n
            
    return np.array(filho)

def mutation_swap(individuo, taxa_mutacao):
    """Mutação por troca de posição entre duas cidades (swap)."""
    if random.random() < taxa_mutacao:
        n = len(individuo)
        idx1, idx2 = random.sample(range(n), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

def selecao_torneio(populacao, aptidoes, k=3):
    """Seleção por torneio."""
    selecionados = random.sample(range(len(populacao)), k)
    vencedor = selecionados[0]
    for i in selecionados[1:]:
        if aptidoes[i] < aptidoes[vencedor]:
            vencedor = i
    return populacao[vencedor]

def algoritmo_genetico(cities, distance_matrix, tam_pop=100, num_geracoes=1000, mutation_rate=0.2):
    """Interface principal do Algoritmo Genético com visualização em tempo real."""
    num_cities = len(cities)
    populacao = gera_populacao_inicial(num_cities, tam_pop)
    aptidoes = [fitness(ind, distance_matrix) for ind in populacao]
    
    best_idx = np.argmin(aptidoes)
    best_route = populacao[best_idx].copy()
    best_distance = aptidoes[best_idx]
    
    # Listas para histórico de visualização
    best_fitness_history = []
    std_fitness_history = []
    
    # Loop de gerações
    
    for gen in range(num_geracoes):
        nova_populacao = []
        # Elitismo: mantém o melhor
        nova_populacao.append(best_route.copy())
        
        while len(nova_populacao) < tam_pop:
            p1 = selecao_torneio(populacao, aptidoes)
            p2 = selecao_torneio(populacao, aptidoes)
            
            filho = crossover_ox(p1, p2)
            filho = mutation_swap(filho, mutation_rate)
            nova_populacao.append(filho)
            
        populacao = nova_populacao
        aptidoes = [fitness(ind, distance_matrix) for ind in populacao]
        
        best_gen_idx = np.argmin(aptidoes)
        if aptidoes[best_gen_idx] < best_distance:
            best_distance = aptidoes[best_gen_idx]
            best_route = populacao[best_gen_idx].copy()
            
        # Coleta dados para os gráficos
        best_fitness_history.append(best_distance)
        std_fitness_history.append(np.std(aptidoes))
            
        # if gen % 100 == 0: # Sobrescrevendo o gráfico anterior
        #     clear_output(wait=True)
        #     print(f"GA Geração {gen}: Melhor distância = {best_distance:.2f}")
        #     plot_ga_figure(cities, best_route, 
        #                    best_fitness_history, std_fitness_history, aptidoes)
            

    return best_route, best_distance

def run_genetic_algorithm(dataset_name):
    """Função de execução do GA com parâmetros escalonados pelo número de cidades."""
    cities = get_tsp_data(dataset_name)
    num_cities = len(cities)
    distance_matrix, _ = generate_distance_matrix(cities)
    
    # Parâmetros adaptativos
    tam_pop = max(50, min(500, num_cities * 5))
    total_calls = num_cities * 15000 
    num_geracoes = total_calls // tam_pop
    
    print(f"Iniciando GA para {dataset_name}: {num_cities} cidades, Pop={tam_pop}, Gen={num_geracoes}...")
    best_route_partial, best_distance = algoritmo_genetico(cities, distance_matrix, 
                                                           tam_pop=tam_pop, 
                                                           num_geracoes=num_geracoes,
                                                           mutation_rate=0.2)
    
    # Reconstrói a rota completa para retorno
    best_route = np.insert(best_route_partial, 0, 0)
    print("GA Best route:", best_route)
    print("GA Best distance:", best_distance)
    return best_route, best_distance

#################### EXECUÇÃO GENETIC ALGORITHM ####################
datasets = ['wi29']

best_route_tsp_ga = []
best_distance_tsp_ga = []

for ds in datasets:
    try:
        best_route_tsp_ga, best_distance_tsp_ga = run_genetic_algorithm(dataset_name=ds)
    except Exception as e:
        print(f"Erro crítico ao processar {ds}: {e}")

#################### MELHOR ROTA GENETIC ALGORITHM ####################
print("Melhor caminho:")
plota_rotas(get_tsp_data('wi29'), best_route_tsp_ga, "Genetic Algorithm")
print("\n")

#################### BOXPLOT GENETIC ALGORITHM ####################
print("boxplot_sorted:")
boxplot_sorted(df=best_route_tsp_ga)
print("\n") 

#################### TABELA GENETIC ALGORITHM ####################
print("Representação do Estado (Figura 4):")
df_estado = pd.DataFrame([best_route_tsp_ga])
print(df_estado.to_string(index=False, header=False))

print("\nTabela com dados GA (Resumo dos Trechos):")
# Utiliza a rota atual para calcular estatísticas dos segmentos (trechos)
cities_xy = get_tsp_data(datasets[0])
dists_ga = [np.linalg.norm(cities_xy[best_route_tsp_ga[i]] - cities_xy[best_route_tsp_ga[(i+1)%len(best_route_tsp_ga)]]) for i in range(len(best_route_tsp_ga))]
df_custo = pd.DataFrame({'Genetic Algorithm (Segmentos)': dists_ga})
print(df_custo.describe().rename(index={'mean': 'Méd', '50%': 'Mediana', 'std': 'Std', '25%': 'Q1 (25%)', '75%': 'Q3 (75%)', 'min': 'Mín', 'max': 'Máx'}))
print("\n")

#################### ESTUDO COMPARATIVO E AUTOMAÇÃO AVANÇADA ####################
import json
import time
from datetime import datetime
import seaborn as sns

def automacao_estudo(dataset_name, num_execs=20):
    """
    Executa um estudo comparativo avançado (SA vs GA).
    Inclui curvas de média (Seaborn), comparação Inicial/Final (Fig 3 e 4) e logs JSON.
    """
    cities = get_tsp_data(dataset_name)
    num_cities = len(cities)
    distance_matrix, _ = generate_distance_matrix(cities)
    total_calls_target = num_cities * 15000
    
    # Parâmetros SA
    sa_iters = num_cities * 500
    sa_nrep = 20 #total_calls_target // sa_iters
    
    # Parâmetros GA
    ga_pop = max(50, min(500, num_cities * 5))
    ga_gens = total_calls_target // ga_pop
    
    log_comparativo = {
        "dataset": dataset_name,
        "num_cities": num_cities,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "runs": []
    }

    print(f"\nIniciando Estudo Comparativo Avançado: {dataset_name} ({num_execs} execuções)...")
    
    sa_results, ga_results = [], []
    sa_hists_df, ga_hists_df = [], []
    
    # Amostras para Figura 3 e 4 (primeira execução)
    sa_sample = {"inicial": None, "final": None}
    ga_sample = {"inicial": None, "final": None}

    for i in range(num_execs):
        print(f"Execução {i+1}/{num_execs}...", end="\r")
        
        # --- EXECUÇÃO SA ---
        # Estado Inicial
        init_route_sa = np.random.permutation(num_cities)
        init_dist_sa = total_distance(init_route_sa, distance_matrix)
        
        if i == 0: sa_sample["inicial"] = (init_route_sa.copy(), init_dist_sa)
        
        curr_route_sa = init_route_sa.copy()
        curr_dist_sa = init_dist_sa
        best_route_sa = curr_route_sa.copy()
        best_dist_sa = curr_dist_sa
        
        temp = 1000.0
        calls_sa = 0
        for it in range(sa_iters):
            for _ in range(sa_nrep):
                neighbor = generate_neighbor(curr_route_sa)
                dist_n = total_distance(neighbor, distance_matrix)
                calls_sa += 1
                if dist_n < curr_dist_sa or random.random() < math.exp((curr_dist_sa - dist_n) / temp):
                    curr_route_sa, curr_dist_sa = neighbor, dist_n
                if curr_dist_sa < best_dist_sa:
                    best_dist_sa, best_route_sa = curr_dist_sa, curr_route_sa.copy()
            temp *= 0.9997
            sa_hists_df.append({"Calls": calls_sa, "Fitness": best_dist_sa, "Algorithm": "SA"})
        
        if i == 0: sa_sample["final"] = (best_route_sa.copy(), best_dist_sa)
        sa_results.append(best_dist_sa)

        # --- EXECUÇÃO GA ---
        # Estado Inicial
        pop = [gera_individuo(num_cities) for _ in range(ga_pop)]
        apt = [fitness(ind, distance_matrix) for ind in pop]
        calls_ga = ga_pop
        
        best_idx = np.argmin(apt)
        best_dist_ga = apt[best_idx]
        best_route_ga_p = pop[best_idx].copy()
        
        if i == 0: 
            init_full_ga = np.insert(pop[0], 0, 0)
            ga_sample["inicial"] = (init_full_ga, apt[0])
            
        ga_hists_df.append({"Calls": calls_ga, "Fitness": best_dist_ga, "Algorithm": "GA"})
        
        for gen in range(ga_gens):
            nova_pop = [best_route_ga_p.copy()]
            while len(nova_pop) < ga_pop:
                p1, p2 = selecao_torneio(pop, apt), selecao_torneio(pop, apt)
                nova_pop.append(mutation_swap(crossover_ox(p1, p2), 0.2))
            pop = nova_pop
            apt = [fitness(ind, distance_matrix) for ind in pop]
            calls_ga += ga_pop
            
            b_gen_idx = np.argmin(apt)
            if apt[b_gen_idx] < best_dist_ga:
                best_dist_ga, best_route_ga_p = apt[b_gen_idx], pop[b_gen_idx].copy()
            ga_hists_df.append({"Calls": calls_ga, "Fitness": best_dist_ga, "Algorithm": "GA"})
            
        if i == 0: 
            final_full_ga = np.insert(best_route_ga_p, 0, 0)
            ga_sample["final"] = (final_full_ga, best_dist_ga)
        ga_results.append(best_dist_ga)

        log_comparativo["runs"].append({
            "id": i + 1, 
            "sa_cost": float(best_dist_sa), 
            "ga_cost": float(best_dist_ga)
        })

    # Salva arquivo de log JSON
    fname = f"estudo_tsp_{dataset_name}_{int(time.time())}.json"
    with open(fname, 'w') as f:
        json.dump(log_comparativo, f, indent=4)
    print(f"\nEstudo concluído! Log salvo em: {fname}")

    # --- RESULTADOS VISUAIS ---
    print("\nVisualizando Comparação Inicial vs Final (Figura 3 e 4)...")
    plot_comparacao_inicial_final(cities, sa_sample["inicial"], sa_sample["final"], "Simulated Annealing")
    plot_comparacao_inicial_final(cities, ga_sample["inicial"], ga_sample["final"], "Genetic Algorithm")
    
    print("\nGerando Gráficos de Convergência...")
    plot_convergencia_estatistica(sa_hists_df, ga_hists_df, dataset_name)
    
    print("\nExibindo Resumo Estatístico Final...")
    display_summary_comparison(sa_results, ga_results, dataset_name)

def plot_comparacao_inicial_final(cities_xy, init_data, final_data, algo):
    """Gera visualização lado a lado (Caminho + Sequência Texto) conforme Fig 3 e 4."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    for ax, data, title in zip([ax1, ax2], [init_data, final_data], ["Inicial", "Final"]):
        route, dist = data
        coords = cities_xy[route]
        # Fechar o ciclo para o plot
        full_coords = np.vstack([coords, coords[0]])
        ax.plot(full_coords[:,0], full_coords[:,1], 'o-', color='tab:blue', markersize=4, alpha=0.6)
        
        # Adiciona a ordem das cidades no gráfico
        for i, (x_i, y_i) in enumerate(coords):
            ax.text(x_i, y_i, f" {i}", fontsize=8, color='darkred', weight='bold')
            
        ax.set_title(f"{algo} - Estado {title}\nTour Length: {dist:.3f}", fontsize=14)
        
        # Representação do Estado em Texto (Figura 4)
        # Mostra apenas as primeiras 15 cidades se o dataset for grande
        trunc = 15
        rep_text = " -> ".join(map(str, route[:trunc])) + ("..." if len(route) > trunc else "")
        ax.text(0.5, -0.15, f"Representação do Estado:\n[{rep_text}]", 
                transform=ax.transAxes, ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.show()

def plot_convergencia_estatistica(sa_hists, ga_hists, dataset):
    """Gráfico de Média com Intervalo de Variação usando Seaborn."""
    df_sa = pd.DataFrame(sa_hists)
    df_ga = pd.DataFrame(ga_hists)
    df_total = pd.concat([df_sa, df_ga])

    plt.figure(figsize=(12, 6))
    if sns is not None:
        sns.lineplot(data=df_total, x="Calls", y="Fitness", hue="Algorithm", estimator="mean", errorbar="sd")
        plt.title(f"Convergência Média com Desvio Padrão - {dataset}", fontsize=15)
    else:
        # Fallback se seaborn não estiver disponível
        for label, df in [("SA", df_sa), ("GA", df_ga)]:
            grouped = df.groupby("Calls")["Fitness"].agg(["mean", "std"])
            plt.plot(grouped.index, grouped["mean"], label=f"{label} (Média)")
            plt.fill_between(grouped.index, grouped["mean"] - grouped["std"], 
                             grouped["mean"] + grouped["std"], alpha=0.2)
        plt.title(f"Convergência Média (Intervalo std) - {dataset} [Matplotlib Fallback]", fontsize=15)
        plt.legend()

    plt.xlabel("Chamadas à Função Objetivo", fontsize=12)
    plt.ylabel("Melhor Fitness", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.show()

def display_summary_comparison(sa_res, ga_res, dataset):
    """Exibe tabela de comparação estatística conforme describe()."""
    df = pd.DataFrame({'Simulated Annealing': sa_res, 'Genetic Algorithm': ga_res})
    desc = df.describe().rename(index={
        'mean': 'Méd', '50%': 'Mediana', 'std': 'Std', 
        '25%': 'Q1 (25%)', '75%': 'Q3 (75%)', 'min': 'Mín', 'max': 'Máx'
    })
    print("\n" + "="*50)
    print(f"RESUMO ESTATÍSTICO DO ESTUDO - {dataset}")
    print("="*50)
    print(desc)
    print("="*50 + "\n")

if __name__ == "__main__":
    automacao_estudo('wi29', num_execs=20)
