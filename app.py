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
    chrom = st.number_input("Cromossomo:", min_value=1, max_value=22, step=1)
    start = st.text_input("Start Position (com pontuação):")
    end = st.text_input("End Position (com pontuação):")
    submit_button = st.form_submit_button("Adicionar Segmento")
    
    if submit_button:
        try:
            start_int = int(start.replace(".", ""))
            end_int = int(end.replace(".", ""))
            if end_int > start_int and chrom in chromosome_sizes:
                st.session_state["comparisons"].append({"Chr": chrom, "Start": start, "End": end, "Comparison": person})
            else:
                st.error("Erro: O End Position deve ser maior que o Start Position e o cromossomo deve ser válido.")
        except ValueError:
            st.error("Erro: Certifique-se de que os valores de Start e End estão corretos e contêm apenas números e pontos.")

# Converter os dados para um DataFrame
if st.session_state["comparisons"]:
    df = pd.DataFrame(st.session_state["comparisons"])
    
    st.write("### Dados Inseridos")
    st.dataframe(df)
    
    # Criar o gráfico único mostrando todos os cromossomos
    fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste do tamanho geral
    
    # Criar um dicionário de cores para cada comparação
    unique_comparisons = df["Comparison"].unique()
    color_map = {comp: np.random.rand(3,) for comp in unique_comparisons}
    
    y_offset = 0  # Posição inicial no eixo Y para organizar os cromossomos
    
    for chrom, chrom_length in chromosome_sizes.items():
        ax.add_patch(plt.Rectangle((0, y_offset), chrom_length, 0.4, color="lightgray", alpha=0.5))  # Linha base do cromossomo
        chrom_data = df[df["Chr"] == chrom]
        
        for _, row in chrom_data.iterrows():
            color = color_map[row["Comparison"]]
            ax.add_patch(plt.Rectangle((int(row["Start"].replace(".", "")), y_offset), 
                                       int(row["End"].replace(".", "")) - int(row["Start"].replace(".", "")), 0.4, color=color, alpha=0.8))
        
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
    st.write(f"🔹 **Número de pessoas comparadas:** {df['Comparison'].nunique()}")
