import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# CSV
data = {
    "aluno_id": list(range(1, 51)),
    "tempo_espera": [1, 3, 1, 2, 3, 1, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 3, 1, 2, 2, 3,
                     1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 2, 1, 2, 1, 1, 1, 0, 0],
    "tempo_atendimento": [12, 15, 15, 13, 19, 41, 13, 12, 13, 24, 29, 41, 12, 12, 15, 29, 36, 36,
                          36, 16, 18, 19, 31, 29, 29, 22, 36, 21, 23, 12, 21, 21, 23, 25, 24, 26,
                          27, 28, 10, 19, 20, 13, 15, 25, 19, 33, 19, 17, 25, 24],
    "tempo_sistema": [13, 18, 16, 15, 22, 42, 13, 12, 13, 25, 31, 44, 15, 14, 16, 29, 36, 36, 36,
                      16, 21, 20, 33, 31, 32, 23, 36, 21, 23, 12, 22, 22, 24, 26, 25, 27, 28, 30,
                      10, 19, 20, 15, 17, 26, 21, 34, 20, 18, 25, 24]
}

df = pd.DataFrame(data)

# Cálculo das métricas M/M/c
def mmc_metrics(arrival_rate, service_rate, c):
    rho = arrival_rate / (c * service_rate)
    sum_terms = sum((arrival_rate / service_rate) ** n / math.factorial(n) for n in range(c))
    last_term = ((arrival_rate / service_rate) ** c) / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sum_terms + last_term)
    Lq = (P0 * ((arrival_rate / service_rate) ** c) * rho) / (math.factorial(c) * ((1 - rho) ** 2))
    Wq = Lq / arrival_rate
    W = Wq + 1 / service_rate
    L = arrival_rate * W
    P_espera = (((arrival_rate / service_rate) ** c) / (math.factorial(c) * (1 - rho))) * P0
    return {"P0": P0, "P_espera": P_espera, "Lq": Lq, "Wq": Wq, "W": W, "L": L, "rho": rho}

# Estimativas
media_chegada = 1 / (df.shape[0] / df['tempo_sistema'].sum())
media_servico = 1 / df['tempo_atendimento'].mean()
chegada_rate = 1 / media_chegada
servico_rate = 1 / df['tempo_atendimento'].mean()

# Métricas
metrics_1 = mmc_metrics(chegada_rate, servico_rate, c=1)
metrics_2 = mmc_metrics(chegada_rate, servico_rate, c=2)

# CSV com métricas
metrics_df = pd.DataFrame([metrics_1, metrics_2], index=["1 servidor", "2 servidores"])
metrics_df.to_csv("resultados_simulacao.csv")

# Gráfico 1 - Tempo de espera por cliente
plt.figure(figsize=(10, 6))
plt.bar(df['aluno_id'], df['tempo_espera'], color='orange')
plt.xlabel('Aluno ID')
plt.ylabel('Tempo de Espera (min)')
plt.title('Tempo de Espera por Cliente')
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_tempo_espera_por_cliente.png")

# Gráfico 2 - Tamanho da fila ao longo do tempo
fila_tempo = []
fila_atual = 0
for i, tempo_espera in enumerate(df['tempo_espera']):
    fila_atual += 1 if tempo_espera > 0 else 0
    fila_tempo.append(fila_atual)
    if tempo_espera == 0:
        fila_atual = max(fila_atual - 1, 0)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 51), fila_tempo, marker='o', linestyle='-', color='green')
plt.xlabel('Cliente')
plt.ylabel('Tamanho da Fila')
plt.title('Tamanho da Fila ao Longo do Tempo')
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_tamanho_fila_tempo.png")

# Gráfico 3 - Tempo de ocupação dos servidores
tempo_ocupacao = np.cumsum(df['tempo_atendimento'])
plt.figure(figsize=(10, 6))
plt.plot(df['aluno_id'], tempo_ocupacao, marker='s', linestyle='-', color='blue')
plt.xlabel('Aluno ID')
plt.ylabel('Tempo Acumulado de Ocupação (min)')
plt.title('Tempo de Ocupação dos Servidores')
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_tempo_ocupacao_servidores.png")
