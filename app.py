import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração inicial do Streamlit
st.title("🔬 Visualizador de Mapa Cromossômico - Estilo Avançado")
st.write("Faça upload de um arquivo CSV contendo os segmentos de DNA para visualizar cada cromossomo individualmente.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])

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
        # Normalizando os valores para visualização
        df["Start"] = df["Start"].str.replace(".", "", regex=False).astype(int)
        df["End"] = df["End"].str.replace(".", "", regex=False).astype(int)
        df["Length"] = df["End"] - df["Start"]
        
        # Criar um gráfico para cada cromossomo individualmente
        chroms = df["Chr"].unique()
        
        for chrom in chroms:
            st.write(f"## Cromossomo {chrom}")
            chrom_data = df[df["Chr"] == chrom]
            
            fig, ax = plt.subplots(figsize=(12, 2))  # Ajuste do tamanho
            max_length = chrom_data["End"].max()
            
            # Criando uma linha de referência preta (cromossomo base)
            ax.add_patch(plt.Rectangle((0, 0.4), max_length, 0.2, color="black", alpha=0.8))
            
            # Adicionando segmentos coloridos
            colors = ["blue", "red", "yellow", "green"]  # Paleta personalizada
            for i, row in chrom_data.iterrows():
                color = np.random.choice(colors)
                ax.add_patch(plt.Rectangle((row["Start"], 0.4), row["End"] - row["Start"], 0.2, color=color, alpha=0.8))
            
            ax.set_xlim(0, max_length)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel("Posição no Cromossomo")
            ax.set_title(f"Visualização do Cromossomo {chrom}")
            
            st.pyplot(fig)
        
        # Estatísticas gerais
        st.write("### 📊 Estatísticas")
        st.write(f"🔹 **Total de segmentos analisados:** {len(df)}")
        st.write(f"🔹 **Número de cromossomos únicos:** {df['Chr'].nunique()}")
