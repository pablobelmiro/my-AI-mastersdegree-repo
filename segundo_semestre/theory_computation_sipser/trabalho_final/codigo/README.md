# Núcleo determinístico reprodutível — experimento

Demonstração, **sem LLM e sem rede**, da teoria do artigo (verificação de
restrições como monitoramento por autômatos). Realiza: parser/GLC (monitor
gramatical = papel do VPA), monitor AFD do laço (R1/R2) e interpretador de
referência (semântica `nested` correlacionada × achatada), produzindo métricas
estruturais reprodutíveis (Parse Rate, EX por nível, falso positivo de T2).

## Como rodar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute experimento.ipynb --output experimento.ipynb
```

Ou abra `experimento.ipynb` no Jupyter/Colab e execute as células 00–06 em ordem.
As figuras são salvas em `figs/`. O notebook contém `assert`s que travam as
propriedades demonstradas; a saída é idêntica a cada execução (determinístico).

## Arquivos

- `experimento.ipynb` — notebook (células 00_setup … 06_figuras).
- `build_notebook.py` — gerador do notebook (regenera o .ipynb).
- `requirements.txt` — dependências (lark, matplotlib, jupyter, nbconvert).
- `figs/` — figuras geradas.

Lê as 10 NF-e reais de `../notas_fiscais/`. A geração C0/C2 por LLM real e o
Elasticsearch real são fase posterior (dissertação).
