import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import random
import math
import time
import json
import pandas as pd
from datetime import datetime
import seaborn as sns

# =============================================================================
# 1. DEFINIÇÃO DA FUNÇÃO DE RASTRIGIN
# =============================================================================
def rastrigin(x, y):
    """
    Função de Rastrigin: f(x,y) = 20 + x^2 - 10*cos(2*pi*x) + y^2 - 10*cos(2*pi*y)
    Mínimo global em (0,0) onde f(0,0) = 0.
    """
    return 20 + x**2 - 10*np.cos(2*np.pi*x) + y**2 - 10*np.cos(2*np.pi*y)

# =============================================================================
# 2. VISUALIZAÇÃO 3D EM TEMPO REAL
# =============================================================================
def plot_rastrigin_3d(current_points, title, ax=None, history=None):
    """
    Desenha a superfície de Rastrigin e os pontos (indivíduos) atuais.
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
    
    # Domínio de busca
    x_range = np.linspace(-5.12, 5.12, 100)
    y_range = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = rastrigin(X, Y)
    
    # Superfície
    ax.plot_surface(X, Y, Z, cmap=cm.magma, alpha=0.4, antialiased=True)
    
    # Pontos atuais (SA: 1 ponto, GA: nuvem de pontos)
    pts = np.atleast_2d(current_points)
    z_pts = rastrigin(pts[:, 0], pts[:, 1])
    ax.scatter(pts[:, 0], pts[:, 1], z_pts, color='cyan', s=50, edgecolors='black', label='Indivíduos')
    
    # Histórico (rastro)
    if history is not None and len(history) > 1:
        h_pts = np.array(history)
        h_z = rastrigin(h_pts[:, 0], h_pts[:, 1])
        ax.plot(h_pts[:, 0], h_pts[:, 1], h_z, color='red', alpha=0.6, linewidth=1, label='Trajetória')

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y)')
    ax.set_zlim(0, 80)
    
# =============================================================================
# 3. SIMULATED ANNEALING (SA)
# =============================================================================
def run_simulated_annealing(iters=1000, visual=True):
    """
    Simulated Annealing com probabilidade de aceitação linear.
    """
    curr_x = random.uniform(-5.12, 5.12)
    curr_y = random.uniform(-5.12, 5.12)
    curr_fit = rastrigin(curr_x, curr_y)
    
    best_x, best_y, best_fit = curr_x, curr_y, curr_fit
    history = [[curr_x, curr_y]]
    fit_history = []
    
    for i in range(iters):
        # Geração de vizinho: x + N(0, 0.2)
        next_x = np.clip(curr_x + np.random.normal(0, 0.2), -5.12, 5.12)
        next_y = np.clip(curr_y + np.random.normal(0, 0.2), -5.12, 5.12)
        next_fit = rastrigin(next_x, next_y)
        
        # Probabilidade de aceitação P(pior)
        if i < 900:
            p_accept = 1.0 - (i / 900.0)
        else:
            p_accept = 0.0
            
        if next_fit < curr_fit:
            curr_x, curr_y, curr_fit = next_x, next_y, next_fit
        elif random.random() < p_accept:
            curr_x, curr_y, curr_fit = next_x, next_y, next_fit
            
        if curr_fit < best_fit:
            best_x, best_y, best_fit = curr_x, curr_y, curr_fit
            
        history.append([curr_x, curr_y])
        fit_history.append({"Step": i, "Fitness": best_fit, "Algorithm": "SA"})
        
        if visual and i % 100 == 0:
            # clear_output(wait=True)
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            plot_rastrigin_3d([curr_x, curr_y], f"SA Iteração {i}\nBest Fit: {best_fit:.4f}", ax, history)
            plt.show()
            
    return [best_x, best_y], best_fit, fit_history

# =============================================================================
# 4. ALGORITMO GENÉTICO (GA)
# =============================================================================
def crossover_blend(p1, p2):
    """Crossover por média ponderada: c = p1*alpha + p2*(1-alpha)"""
    alpha = random.random()
    c1 = p1 * alpha + p2 * (1 - alpha)
    c2 = p2 * alpha + p1 * (1 - alpha)
    return c1, c2

def mutation_normal(ind, rate=0.2):
    """Mutação baseada em distribuição normal N(0, 0.2)"""
    if random.random() < rate:
        ind = ind + np.random.normal(0, 0.2, size=2)
        ind = np.clip(ind, -5.12, 5.12)
    return ind

def run_genetic_algorithm(pop_size=20, gens=50, mut_rate=0.2, visual=True):
    """
    Algoritmo Genético para otimização contínua.
    """
    # População inicial
    pop = np.random.uniform(-5.12, 5.12, (pop_size, 2))
    fits = np.array([rastrigin(ind[0], ind[1]) for ind in pop])
    
    best_idx = np.argmin(fits)
    best_ind = pop[best_idx].copy()
    best_fit = fits[best_idx]
    fit_history = []
    
    for g in range(gens):
        new_pop = []
        # Elitismo
        new_pop.append(best_ind.copy())
        
        while len(new_pop) < pop_size:
            # Seleção (Torneio simples de 2)
            i1, i2 = random.sample(range(pop_size), 2)
            p1 = pop[i1] if fits[i1] < fits[i2] else pop[i2]
            
            i3, i4 = random.sample(range(pop_size), 2)
            p2 = pop[i3] if fits[i3] < fits[i4] else pop[i4]
            
            # Crossover
            c1, c2 = crossover_blend(p1, p2)
            
            # Mutação
            new_pop.append(mutation_normal(c1, mut_rate))
            if len(new_pop) < pop_size:
                new_pop.append(mutation_normal(c2, mut_rate))
                
        pop = np.array(new_pop)
        fits = np.array([rastrigin(ind[0], ind[1]) for ind in pop])
        
        b_idx = np.argmin(fits)
        if fits[b_idx] < best_fit:
            best_fit = fits[b_idx]
            best_ind = pop[b_idx].copy()
            
        # Sincroniza iterações do GA com SA (pop_size avaliações por geração)
        fit_history.append({"Step": g * pop_size, "Fitness": best_fit, "Algorithm": "GA"})
        
        if visual and g % 10 == 0:
            # clear_output(wait=True)
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            plot_rastrigin_3d(pop, f"GA Geração {g}\nBest Fit: {best_fit:.4f}", ax)
            plt.show()
            
    return best_ind, best_fit, fit_history

# =============================================================================
# 5. ESTUDO COMPARATIVO E AUTOMAÇÃO
# =============================================================================
def plot_convergence_curves(sa_hist, ga_hist):
    """Gera curvas de convergência média com intervalos de variação."""
    df_total = pd.DataFrame(sa_hist + ga_hist)
    plt.figure(figsize=(12, 6))
    if sns is not None:
        sns.lineplot(data=df_total, x="Step", y="Fitness", hue="Algorithm", estimator="mean", errorbar="sd")
        plt.title("Curva de Convergência Média (com Desvio Padrão)", fontsize=14)
    else:
        for algo in ["SA", "GA"]:
            df_algo = df_total[df_total["Algorithm"] == algo]
            grouped = df_algo.groupby("Step")["Fitness"].agg(["mean", "std"])
            plt.plot(grouped.index, grouped["mean"], label=f"{algo} (Méd)")
            plt.fill_between(grouped.index, grouped["mean"] - grouped["std"], grouped["mean"] + grouped["std"], alpha=0.2)
        plt.title("Curva de Convergência Média [Matplotlib Fallback]", fontsize=14)
        plt.legend()
    
    plt.xlabel("Avaliações da Função Objetivo / Etapas", fontsize=12)
    plt.ylabel("Custo (Aptidão)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_comparacao_inicial_final(initial_data, final_data, algo_name):
    """Gera visualização lado a lado do estado inicial vs final na superfície de Rastrigin."""
    fig = plt.figure(figsize=(16, 8))
    
    # Estado Inicial
    ax1 = fig.add_subplot(121, projection='3d')
    coords_init, fit_init = initial_data
    plot_rastrigin_3d(coords_init, f"{algo_name} - Estado Inicial\nFitness: {fit_init:.4f}", ax1)
    
    # Estado Final
    ax2 = fig.add_subplot(122, projection='3d')
    coords_final, fit_final = final_data
    # Para o estado final, se for SA (ponto único), podemos passar o histórico se disponível, 
    # mas aqui simplificamos para o ponto final.
    plot_rastrigin_3d(coords_final, f"{algo_name} - Estado Final\nFitness: {fit_final:.4f}", ax2)
    
    plt.tight_layout()
    plt.show()

def display_summary_comparison(sa_res, ga_res):
    """Exibe tabela de comparação estatística traduzida."""
    df = pd.DataFrame({'Simulated Annealing': sa_res, 'Genetic Algorithm': ga_res})
    desc = df.describe().rename(index={
        'mean': 'Méd', 'std': 'Std', 'min': 'Mín', 
        '25%': 'Q1 (25%)', '50%': 'Mediana', '75%': 'Q3 (75%)', 'max': 'Máx'
    })
    print("\n" + "="*50)
    print("RESUMO ESTATÍSTICO DOS RESULTADOS - RASTRIGIN")
    print("="*50)
    print(desc)
    print("="*50 + "\n")

def plot_boxplot_comparison(sa_res, ga_res, problem_name="Rastrigin"):
    """Gera boxplot comparativo estilizado conforme referência (Padronizado)."""
    data = [sa_res, ga_res]
    labels = ['Simulated Annealing', 'Genetic Algorithm']
    
    plt.figure(figsize=(10, 7))
    
    # Estilização idêntica à referência da Figura 1
    box_props = dict(linestyle='-', linewidth=2, color='cornflowerblue')
    whisker_props = dict(linestyle='-', linewidth=2, color='cornflowerblue')
    capprops = dict(linestyle='-', linewidth=2, color='cornflowerblue')
    median_props = dict(linestyle='-', linewidth=2, color='firebrick')
    flier_props = dict(marker='o', markerfacecolor='dimgray', markersize=6, linestyle='none')

    plt.boxplot(data, labels=labels, patch_artist=False,
                boxprops=box_props, whiskerprops=whisker_props,
                capprops=capprops, medianprops=median_props,
                flierprops=flier_props)
        
    plt.title(f"Cost of Algorithms - {problem_name}", fontsize=16)
    plt.ylabel("Custo (Fitness)", fontsize=12)
    plt.grid(True, linestyle='-', alpha=0.3)
    
    # Rotação vertical para as labels
    plt.xticks(rotation=90)
    
    plt.tight_layout()
    plt.show()

def display_config_comparison():
    """Tabela comparativa de configurações (Padrão TSP)."""
    configs = {
        "Parâmetro": ["População", "Gerações / Iterações", "Operador Mutação", "Operador Crossover", "Resfriamento / Seleção"],
        "SA": ["1 (Ponto Único)", "1000", "N(0, 0.2)", "N/A", "Linear Decay"],
        "GA": ["20", "50", "N(0, 0.2)", "Blend Mix", "Torneio (k=2)"]
    }
    print("\n" + "="*65)
    print("CONFIGURAÇÃO DOS ALGORITMOS NO ESTUDO (RASTRIGIN)")
    print("="*65)
    print(pd.DataFrame(configs).to_string(index=False))
    print("="*65 + "\n")

def automacao_estudo(num_execs=20):
    """
    Executa o estudo comparativo SA vs GA com análise aprofundada (Padrão TSP).
    """
    global RESULTADOS_SA, RESULTADOS_GA
    RESULTADOS_SA, RESULTADOS_GA = [], []
    HISTS_SA, HISTS_GA = [], []
    
    sa_sample = {"inicial": None, "final": None}
    ga_sample = {"inicial": None, "final": None}
    
    log = {
        "algoritmo": "Rastrigin Minimization",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "execuções": []
    }
    
    print(f"\nIniciando Estudo Comparativo Avançado: Rastrigin ({num_execs} execuções)...")
    
    for i in range(num_execs):
        print(f"Trial {i+1}/{num_execs}...", end="\r")
        
        # --- EXECUÇÃO SA ---
        # Amostra inicial (apenas na primeira execução)
        if i == 0:
            init_x, init_y = random.uniform(-5.12, 5.12), random.uniform(-5.12, 5.12)
            sa_sample["inicial"] = ([init_x, init_y], rastrigin(init_x, init_y))
            # Reiniciamos a busca a partir deste ponto para o primeiro trial real
            curr_x, curr_y = init_x, init_y
        
        best_coords_sa, fit_sa, hist_sa = run_simulated_annealing(iters=1000, visual=False)
        RESULTADOS_SA.append(fit_sa)
        HISTS_SA.extend(hist_sa)
        if i == 0: sa_sample["final"] = (best_coords_sa, fit_sa)
        
        # --- EXECUÇÃO GA ---
        # Amostra inicial (apenas na primeira execução)
        if i == 0:
            init_pop = np.random.uniform(-5.12, 5.12, (20, 2))
            init_fits = np.array([rastrigin(ind[0], ind[1]) for ind in init_pop])
            ga_sample["inicial"] = (init_pop, np.min(init_fits))
        
        best_coords_ga, fit_ga, hist_ga = run_genetic_algorithm(pop_size=20, gens=50, visual=False)
        RESULTADOS_GA.append(fit_ga)
        HISTS_GA.extend(hist_ga)
        if i == 0: ga_sample["final"] = (best_coords_ga, fit_ga)
        
        log["execuções"].append({"trial": i+1, "sa_fit": float(fit_sa), "ga_fit": float(fit_ga)})
        
    # Salva JSON
    fname = f"estudo_rastrigin_{int(time.time())}.json"
    with open(fname, 'w') as f: json.dump(log, f, indent=4)
    print(f"\nEstudo concluído! Log salvo em {fname}")
    
    # --- RESULTADOS VISUAIS E ESTATÍSTICOS ---
    display_config_comparison()
    plot_convergence_curves(HISTS_SA, HISTS_GA)
    
    print("\nVisualizando Comparação Inicial vs Final (Estado do primeiro Trial)...")
    plot_comparacao_inicial_final(sa_sample["inicial"], sa_sample["final"], "Simulated Annealing")
    plot_comparacao_inicial_final(ga_sample["inicial"], ga_sample["final"], "Genetic Algorithm")

    # Exibe Boxplot Padronizado
    print("\nVisualizando Distribuição de Resultados (Boxplot)...")
    plot_boxplot_comparison(RESULTADOS_SA, RESULTADOS_GA, "Rastrigin")
    
    display_summary_comparison(RESULTADOS_SA, RESULTADOS_GA)

# =============================================================================
# BLOCO DE EXECUÇÃO
# =============================================================================
    print("Processando demonstração visual SA...")
    run_simulated_annealing(iters=1000, visual=True)
    
    # Demonstração Visual GA
    print("Processando demonstração visual GA...")
    run_genetic_algorithm(pop_size=20, gens=50, visual=True)
    
    # Estudo Comparativo
    automacao_estudo(num_execs=20)