import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Tamanhos reais dos cromossomos (baseado na tabela fornecida)
chromosome_sizes = {
    1: 249154567, 2: 242942878, 3: 197526201, 4: 190685303, 5: 14862533,
    6: 170814183, 7: 158778256, 8: 145919126, 9: 140928675, 10: 135352153,
    11: 134803123, 12: 130100796, 13: 115008038, 14: 105916797, 15: 102247864,
    16: 90103117, 17: 80924707, 18: 77869022, 19: 58864479, 20: 62729431,
    21: 47560946, 22: 51072161
}

# Configuração inicial do Streamlit
st.title("🔬 Visualizador de Mapa Cromossômico - Comparação de Múltiplos DNAs")
st.write("Faça upload de um arquivo CSV contendo as comparações de múltiplos indivíduos para visualizar as coincidências de DNA.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])

if uploaded_file:
    # Ler o CSV com separador de ponto e vírgula
    df = pd.read_csv(uploaded_file, sep=";")
    
    # Exibir os dados carregados
    st.write("### Dados Carregados")
    st.dataframe(df)
    
    # Verificar se as colunas corretas existem
    expected_columns = {"Chr", "Start", "End", "Comparison"}
    if not expected_columns.issubset(df.columns):
        st.error("Erro: O arquivo CSV deve conter as colunas 'Chr', 'Start', 'End' e 'Comparison'.")
    else:
        # Garantir que os valores numéricos sejam convertidos corretamente
        df["Chr"] = df["Chr"].astype(float).astype(int)  # Remove .0 e converte para inteiro
        df["Start"] = df["Start"].astype(float).astype(int)  # Converte para inteiro
        df["End"] = df["End"].astype(float).astype(int)  # Converte para inteiro
        df["Length"] = df["End"] - df["Start"]
        
        # Criar o gráfico único mostrando todos os cromossomos
        fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste do tamanho geral
        
        # Criar um dicionário de cores para cada comparação
        comparisons = df["Comparison"].unique()
        color_map = {comp: np.random.rand(3,) for comp in comparisons}
        
        y_offset = 0  # Posição inicial no eixo Y para organizar os cromossomos
        
        for chrom, chrom_length in chromosome_sizes.items():
            ax.add_patch(plt.Rectangle((0, y_offset), chrom_length, 0.4, color="lightgray", alpha=0.5))  # Linha base do cromossomo
            chrom_data = df[df["Chr"] == chrom]
            
            for _, row in chrom_data.iterrows():
                color = color_map[row["Comparison"]]
                ax.add_patch(plt.Rectangle((row["Start"], y_offset), row["End"] - row["Start"], 0.4, color=color, alpha=0.8))
            
            y_offset += 1  # Move para o próximo cromossomo
        
        ax.set_xlim(0, max(chromosome_sizes.values()))
        ax.set_ylim(0, y_offset)
        ax.set_yticks(range(y_offset))
        ax.set_yticklabels([f"Chr {chrom}" for chrom in chromosome_sizes.keys()])
        ax.set_xlabel("Posição no Cromossomo")
        ax.set_title("Comparação de Múltiplos DNAs por Cromossomo")
        
        st.pyplot(fig)
        
        # Estatísticas gerais
        st.write("### 📊 Estatísticas")
        st.write(f"🔹 **Total de segmentos analisados:** {len(df)}")
        st.write(f"🔹 **Número de cromossomos únicos:** {df['Chr'].nunique()}")
        st.write(f"🔹 **Número de pessoas comparadas com Raymundo:** {df['Comparison'].nunique()}")
