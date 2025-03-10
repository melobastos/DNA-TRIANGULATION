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
st.write("Insira manualmente as comparações de DNA para visualizar as coincidências cromossômicas.")

# Lista para armazenar os dados inseridos
if "comparisons" not in st.session_state:
    st.session_state["comparisons"] = []

# Interface para entrada manual de dados
with st.form("dna_input_form"):
    person = st.text_input("Nome da Pessoa Comparada:")
    chrom = st.number_input("Cromossomo:", min_value=1, max_value=22, step=1, format="%d")
    start = st.text_input("Start Position (com pontuação):")
    end = st.text_input("End Position (com pontuação):")
    submit_button = st.form_submit_button("Adicionar Segmento")
    
    if submit_button:
        try:
            start_int = int(start.replace(".", ""))
            end_int = int(end.replace(".", ""))
            if end_int > start_int and chrom in chromosome_sizes:
                st.session_state["comparisons"].append({"Chr": int(chrom), "Start": start_int, "End": end_int, "Comparison": person})
            else:
                st.error("Erro: O End Position deve ser maior que o Start Position e o cromossomo deve ser válido.")
        except ValueError:
            st.error("Erro: Certifique-se de que os valores de Start e End estão corretos e contêm apenas números e pontos.")

# Converter os dados para um DataFrame
if st.session_state["comparisons"]:
    df = pd.DataFrame(st.session_state["comparisons"])
    
    st.write("### Dados Inseridos")
    st.dataframe(df)
    
    # Filtrar apenas os cromossomos que possuem segmentos
    unique_chromosomes = sorted(df["Chr"].unique())
    
    # Criar o gráfico único mostrando apenas os cromossomos relevantes
    fig, ax = plt.subplots(figsize=(12, len(unique_chromosomes) * 0.7))  # Ajuste do tamanho do gráfico
    
    # Criar um dicionário de cores para cada comparação
    unique_comparisons = df["Comparison"].unique()
    color_map = {comp: np.random.rand(3,) for comp in unique_comparisons}
    
    y_positions = {chrom: idx for idx, chrom in enumerate(unique_chromosomes)}  # Correta ordenação vertical
    y_gap = 0.5  # Espaço entre as faixas
    
    for chrom in unique_chromosomes:  # Apenas cromossomos com segmentos
        chrom_length = chromosome_sizes[chrom]
        chrom_data = df[df["Chr"] == chrom]
        y_offset = y_positions[chrom]  # Ajustar corretamente a posição no eixo Y
        
        for _, row in chrom_data.iterrows():
            color = color_map[row["Comparison"]]
            ax.add_patch(plt.Rectangle((row["Start"], y_offset), 
                                       row["End"] - row["Start"], 0.4, color=color, alpha=0.8))
        
    ax.set_xlim(0, max(chromosome_sizes.values()))
    ax.set_ylim(-1, len(unique_chromosomes))
    ax.set_yticks(range(len(unique_chromosomes)))
    ax.set_yticklabels([f"Chr {chrom}" for chrom in unique_chromosomes])
    ax.set_xlabel("Posição no Cromossomo")
    ax.set_title("Comparação de Múltiplos DNAs por Cromossomo")
    
    st.pyplot(fig)
    
    # Exibir legenda separadamente
    st.write("### 🔹 Legenda - Comparações")
    legend_items = []
    for comp, color in color_map.items():
        color_hex = f'rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)})'
        legend_items.append(f"<span style='display: inline-block; width: 20px; height: 20px; background: {color_hex}; margin-right: 10px;'></span>{comp}")
    
    legend_html = "<div style='display: flex; flex-wrap: wrap; gap: 15px;'>" + "".join(legend_items) + "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
    
    # Estatísticas gerais
    st.write("### 📊 Estatísticas")
    st.write(f"🔹 **Total de segmentos analisados:** {len(df)}")
    st.write(f"🔹 **Número de cromossomos exibidos:** {len(unique_chromosomes)}")
    st.write(f"🔹 **Número de pessoas comparadas:** {df['Comparison'].nunique()}")
