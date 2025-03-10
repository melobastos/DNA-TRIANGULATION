import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Título do App
st.title("Visualizador de Mapa Cromossômico")

# Explicação rápida
st.write("Insira uma tabela com as informações de segmentos de DNA para visualizar a posição dos segmentos em cada cromossomo.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Carregue um arquivo CSV", type=["csv"])

if uploaded_file:
    # Ler o CSV com separador de ponto e vírgula
    df = pd.read_csv(uploaded_file, sep=";")

    # Exibir os dados carregados
    st.write("### Dados Carregados")
    st.dataframe(df)

    # Verificar se as colunas corretas existem
    expected_columns = {"Chr", "Start", "End"}
    if not expected_columns.issubset(df.columns):
        st.error("Erro: O arquivo CSV deve conter as colunas 'Chr', 'Start' e 'End'.")
    else:
        # Normalizando os tamanhos para visualização
        df["Start"] = df["Start"].str.replace(".", "", regex=False).astype(int)
        df["End"] = df["End"].str.replace(".", "", regex=False).astype(int)
        df["Length"] = df["End"] - df["Start"]
        max_length = df["Length"].max()
        df["Norm_Length"] = df["Length"] / max_length

        # Criando o gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 8))
        for i, row in df.iterrows():
            ax.add_patch(patches.Rectangle((0, i), row["Norm_Length"], 0.8, color="blue", alpha=0.3))  # Cromossomos

        # Adicionando os segmentos de DNA compartilhados
        for i, row in df.iterrows():
            ax.add_patch(patches.Rectangle((row["Start"] / max_length, i), 
                                           (row["End"] - row["Start"]) / max_length, 0.8, 
                                           color="red", alpha=0.7))  # Segmentos

        # Configurações do eixo
        ax.set_xlim(0, 1)
        ax.set_ylim(-1, len(df))
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels([f"Chr {chr}" for chr in df["Chr"]])
        ax.set_xlabel("Proporção do tamanho do cromossomo")
        ax.set_title("Mapa Visual dos Cromossomos com Segmentos de DNA")

        plt.gca().invert_yaxis()  # Invertendo a ordem para exibição correta

        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
