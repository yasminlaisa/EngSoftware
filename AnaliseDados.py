import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# CSV
df = pd.read_csv("dados_fila.csv")

# Estatísticas descritivas
print("Média Atendimento:", df["tempo_atendimento (minutos)"].mean())
print("Mediana Atendimento:", df["tempo_atendimento (minutos)"].median())
print("Moda Atendimento:", df["tempo_atendimento (minutos)"].mode().iloc[0])
print("Variância Atendimento:", df["tempo_atendimento (minutos)"].var())
print("Desvio Padrão Atendimento:", df["tempo_atendimento (minutos)"].std())

print("Média Espera:", df["tempo_espera (minutos)"].mean())
print("Mediana Espera:", df["tempo_espera (minutos)"].median())
print("Moda Espera:", df["tempo_espera (minutos)"].mode().iloc[0])
print("Variância Espera:", df["tempo_espera (minutos)"].var())
print("Desvio Padrão Espera:", df["tempo_espera (minutos)"].std())

# Intervalo de confiança para a média
conf_att = stats.t.interval(0.95, len(df)-1, loc=df["tempo_atendimento (minutos)"].mean(),
scale=stats.sem(df["tempo_atendimento (minutos)"]))
conf_espera = stats.t.interval(0.95, len(df)-1, loc=df["tempo_espera (minutos)"].mean(),
scale=stats.sem(df["tempo_espera (minutos)"]))

print("IC Atendimento:", conf_att)
print("IC Espera:", conf_espera)

# Histograma
plt.hist(df["tempo_atendimento (minutos)"], bins=10)
plt.title("Histograma - Tempo de Atendimento")
plt.savefig("histograma_tempo_atendimento.png")
plt.clf()

plt.hist(df["tempo_espera (minutos)"], bins=10)
plt.title("Histograma - Tempo de Espera")
plt.savefig("histograma_tempo_espera.png")
plt.clf()

# Boxplot
plt.boxplot([df["tempo_atendimento (minutos)"], df["tempo_espera (minutos)"]],
            labels=["Atendimento", "Espera"])
plt.title("Boxplot - Atendimento vs Espera")
plt.savefig("boxplot_atendimento_espera.png")