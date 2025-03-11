import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
import csv

# Verificar se openpyxl está disponível
try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# Configuração da página (deve ser a primeira instrução Streamlit!)
st.set_page_config(
    page_title="Visualizador de Mapa Cromossômico",
    page_icon="🔬",
    layout="wide"
)

# Tamanhos reais dos cromossomos
chromosome_sizes = {
    1: 249154567, 2: 242942878, 3: 197526201, 4: 190685303, 5: 181538259,
    6: 170814183, 7: 158878256, 8: 145919126, 9: 140928675, 10: 135352153,
    11: 134803123, 12: 130100796, 13: 115008038, 14: 105916797, 15: 102247864,
    16: 90103117, 17: 80924707, 18: 77869022, 19: 58864479, 20: 62729431,
    21: 47560946, 22: 51072161, 'X': 155270560, 'Y': 59373566
}

# Função para gerar cores distintas para cada pessoa
def generate_distinct_colors(n):
    colors = plt.cm.tab20.colors + plt.cm.tab20b.colors
    if n <= len(colors):
        return {i: colors[i] for i in range(n)}
    return {i: np.random.rand(3,) for i in range(n)}

# Função para formatar números grandes com separadores
def format_number(num):
    return f"{num:,}".replace(",", ".")

# Função para converter DataFrame para CSV
def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    processed_data = output.getvalue()
    return processed_data

# Função para formatar ticks do eixo x
def format_x_ticks(x, pos):
    return format_number(int(x))

st.title("🔬 Visualizador de Mapa Cromossômico - Comparação de Múltiplos DNAs")

# Tabs

tab1, tab2, tab3 = st.tabs(["📝 Entrada de Dados", "📊 Visualização", "⚙️ Configurações"])

with tab2:
    if "comparisons" in st.session_state and st.session_state.comparisons:
        df = pd.DataFrame(st.session_state.comparisons)

        all_chromosomes = sorted(df["Chr"].unique(), key=lambda x: (isinstance(x, str), x))
        selected_chromosomes = st.multiselect("Selecionar Cromossomos para Visualizar:", all_chromosomes, default=all_chromosomes)

        filtered_df = df[df["Chr"].isin(selected_chromosomes)]

        if not filtered_df.empty:
            unique_chromosomes = sorted(filtered_df["Chr"].unique(), key=lambda x: (isinstance(x, str), x))
            colors = generate_distinct_colors(len(df["Comparison"].unique()))
            color_map = {name: colors[i] for i, name in enumerate(df["Comparison"].unique())}

            fig_height = max(6, len(unique_chromosomes) * 0.8)
            fig, ax = plt.subplots(figsize=(12, fig_height))

            for idx, chrom in enumerate(unique_chromosomes):
                y_base = idx
                ax.barh(y_base, chromosome_sizes[chrom], height=0.6, color="lightgray")

                chrom_df = filtered_df[filtered_df["Chr"] == chrom]
                for _, row in chrom_df.iterrows():
                    segment_length = row["End"] - row["Start"]
                    ax.add_patch(plt.Rectangle((row["Start"], y_base - 0.3), segment_length, 0.6, color=color_map[row["Comparison"]]))

                    ax.text(
                        row["End"] + chromosome_sizes[chrom] * 0.005,
                        y_base,
                        row["Comparison"],
                        va='center', ha='left', fontsize=7, color='black'
                    )

            ax.set_yticks(range(len(unique_chromosomes)))
            ax.set_yticklabels([f"Chr {chrom}" for chrom in unique_chromosomes])
            ax.set_xlabel("Posição no Cromossomo (pb)")
            ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_ticks))
            ax.grid(axis='x')

            st.pyplot(fig)

            img = BytesIO()
            fig.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            st.download_button("Baixar Imagem do Gráfico", img, "chromosome_map.png", "image/png")
        else:
            st.warning("Nenhum dado disponível para visualização.")
    else:
        st.info("Nenhum dado disponível para visualização. Insira dados primeiro.")
