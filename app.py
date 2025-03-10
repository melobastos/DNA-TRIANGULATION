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
        # Garantir que os valores numéricos sejam tratados corretamente
        df["Chr"] = df["Chr"].astype(str).str.replace(".0", "", regex=False).astype(int)
        df["Start"] = df["Start"].astype(str).str.replace(".", "", regex=False).astype(int)
        df["End"] = df["End"].astype(str).str.replace(".", "", regex=False).astype(int)
        df["Length"] = df["End"] - df["Start"]
        
        # Criar um gráfico para cada cromossomo individualmente, ajustado à escala real
        chroms = df["Chr"].unique()
        
        for chrom in chroms:
            if chrom in chromosome_sizes:
                st.write(f"## Cromossomo {chrom}")
                chrom_data = df[df["Chr"] == chrom]
                chrom_length = chromosome_sizes[chrom]
                
                fig, ax = plt.subplots(figsize=(12, 2))  # Ajuste do tamanho
                
                # Criando uma linha de referência preta (cromossomo base)
                ax.add_patch(plt.Rectangle((0, 0.4), chrom_length, 0.2, color="black", alpha=0.8))
                
                # Adicionando segmentos coloridos por comparação
                comparisons = df["Comparison"].unique()
                color_map = {comp: np.random.rand(3,) for comp in comparisons}  # Gera cores únicas para cada pessoa comparada
                
                for i, row in chrom_data.iterrows():
                    color = color_map[row["Comparison"]]
                    ax.add_patch(plt.Rectangle((row["Start"], 0.4), row["End"] - row["Start"], 0.2, color=color, alpha=0.8))
                
                ax.set_xlim(0, chrom_length)
                ax.set_ylim(0, 1)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_xlabel("Posição no Cromossomo")
                ax.set_title(f"Visualização do Cromossomo {chrom} - Comparação com Raymundo")
                
                st.pyplot(fig)
        
        # Estatísticas gerais
        st.write("### 📊 Estatísticas")
        st.write(f"🔹 **Total de segmentos analisados:** {len(df)}")
        st.write(f"🔹 **Número de cromossomos únicos:** {df['Chr'].nunique()}")
        st.write(f"🔹 **Número de pessoas comparadas com Raymundo:** {df['Comparison'].nunique()}")
