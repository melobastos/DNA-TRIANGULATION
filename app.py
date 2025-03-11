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

# Configuração da página
st.set_page_config(
    page_title="Visualizador de Mapa Cromossômico",
    page_icon="🔬",
    layout="wide"
)

# Tamanhos reais dos cromossomos (baseado na tabela fornecida)
chromosome_sizes = {
    1: 249154567, 2: 242942878, 3: 197526201, 4: 190685303, 5: 181538259,
    6: 170814183, 7: 158878256, 8: 145919126, 9: 140928675, 10: 135352153,
    11: 134803123, 12: 130100796, 13: 115008038, 14: 105916797, 15: 102247864,
    16: 90103117, 17: 80924707, 18: 77869022, 19: 58864479, 20: 62729431,
    21: 47560946, 22: 51072161, 'X': 155270560, 'Y': 59373566
}

# Função para gerar cores distintas para cada pessoa
def generate_distinct_colors(n):
    """Gera cores visualmente distintas."""
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

# Função para converter DataFrame para Excel (apenas se openpyxl estiver disponível)
def convert_df_to_excel(df):
    if not EXCEL_AVAILABLE:
        return None
    output = BytesIO()
    df.to_excel(output, index=False)
    processed_data = output.getvalue()
    return processed_data

# Função para formatar ticks do eixo x
def format_x_ticks(x, pos):
    """Formata os números do eixo X com separadores de milhar"""
    return format_number(int(x))

# Configuração inicial do Streamlit
st.title("🔬 Visualizador de Mapa Cromossômico - Comparação de Múltiplos DNAs")

# Usar tabs para organizar a interface
tab1, tab2, tab3 = st.tabs(["📝 Entrada de Dados", "📊 Visualização", "⚙️ Configurações"])

with tab1:
    st.write("Insira manualmente as comparações de DNA para visualizar as coincidências cromossômicas.")
    
    # Inicializar session state para armazenar dados
    if "comparisons" not in st.session_state:
        st.session_state.comparisons = []
    
    # Opção de upload de CSV
    st.subheader("Importar dados de arquivo")
    
    # Determinar tipos de arquivo aceitos
    file_types = ["csv"]
    if EXCEL_AVAILABLE:
        file_types.append("xlsx")
    
    file_type_str = ", ".join(file_types).upper()
    uploaded_file = st.file_uploader(f"Carregar {file_type_str} com dados", type=file_types)
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                import_df = pd.read_csv(uploaded_file)
            elif EXCEL_AVAILABLE and uploaded_file.name.endswith('.xlsx'):
                import_df = pd.read_excel(uploaded_file)
            else:
                st.error(f"Formato de arquivo não suportado. Use {file_type_str}.")
                import_df = None
            
            # Verificar se as colunas necessárias existem
            if import_df is not None:
                required_cols = ["Chr", "Start", "End", "Comparison"]
                if all(col in import_df.columns for col in required_cols):
                    # Converter para o formato correto
                    for _, row in import_df.iterrows():
                        new_entry = {
                            "Chr": row["Chr"],
                            "Start": int(row["Start"]),
                            "End": int(row["End"]),
                            "Comparison": row["Comparison"]
                        }
                        st.session_state.comparisons.append(new_entry)
                    st.success(f"Importados {len(import_df)} registros com sucesso!")
                else:
                    st.error(f"Formato de arquivo inválido. As colunas devem ser: {', '.join(required_cols)}")
        except Exception as e:
            st.error(f"Erro ao importar arquivo: {e}")
    
    # Interface para entrada manual de dados
    st.subheader("Adicionar dados manualmente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("dna_input_form"):
            person = st.text_input("Nome da Pessoa Comparada:")
            chrom_options = list(range(1, 23)) + ['X', 'Y']
            chrom = st.selectbox("Cromossomo:", chrom_options)
            
            start = st.text_input("Start Position (com pontuação):")
            end = st.text_input("End Position (com pontuação):")
            
            submit_button = st.form_submit_button("Adicionar Segmento")
            
            if submit_button:
                try:
                    # Remover pontuação e converter para inteiro
                    start_int = int(start.replace(".", "").replace(",", ""))
                    end_int = int(end.replace(".", "").replace(",", ""))
                    
                    if end_int > start_int and chrom in chromosome_sizes:
                        st.session_state.comparisons.append({
                            "Chr": chrom, 
                            "Start": start_int, 
                            "End": end_int, 
                            "Comparison": person
                        })
                        st.success("Segmento adicionado com sucesso!")
                    else:
                        st.error("Erro: O End Position deve ser maior que o Start Position e o cromossomo deve ser válido.")
                except ValueError:
                    st.error("Erro: Certifique-se de que os valores de Start e End estão corretos e contêm apenas números e pontos ou vírgulas.")
    
    with col2:
        # Mostrar dados inseridos
        if st.session_state.comparisons:
            df = pd.DataFrame(st.session_state.comparisons)
            st.dataframe(df, use_container_width=True)
            
            # Botão para limpar dados
            if st.button("Limpar todos os dados"):
                st.session_state.comparisons = []
                st.experimental_rerun()
            
            # Botão para exportar dados como CSV
            csv_data = convert_df_to_csv(df)
            st.download_button(
                label="Baixar como CSV",
                data=csv_data,
                file_name='chromosome_data.csv',
                mime='text/csv',
            )
            
            # Botão para exportar dados como Excel (apenas se disponível)
            if EXCEL_AVAILABLE:
                excel_data = convert_df_to_excel(df)
                st.download_button(
                    label="Baixar como Excel",
                    data=excel_data,
                    file_name='chromosome_data.xlsx',
                    mime='application/vnd.ms-excel',
                )
        else:
            st.info("Nenhum dado inserido ainda. Adicione segmentos usando o formulário.")

with tab2:
    # Visualização dos dados
    if "comparisons" in st.session_state and st.session_state.comparisons:
        df = pd.DataFrame(st.session_state.comparisons)
        
        # Configurações de visualização
        st.subheader("Configurações do Gráfico")
        
        col_viz1, col_viz2 = st.columns(2)
        with col_viz1:
            # Opção para filtrar cromossomos
            all_chroms = sorted(list(set(df["Chr"])), key=lambda x: (isinstance(x, str), x))
            selected_chroms = st.multiselect(
                "Selecionar Cromossomos para Visualizar:",
                options=all_chroms,
                default=all_chroms
            )
        
        with col_viz2:
            # Opção para filtrar pessoas
            all_people = sorted(df["Comparison"].unique())
            selected_people = st.multiselect(
                "Selecionar Pessoas para Visualizar:",
                options=all_people,
                default=all_people
            )
        
        # Filtrar dados
        filtered_df = df[
            (df["Chr"].isin(selected_chroms)) & 
            (df["Comparison"].isin(selected_people))
        ]
        
        if not filtered_df.empty:
            unique_chromosomes = sorted(filtered_df["Chr"].unique(), key=lambda x: (isinstance(x, str), x))
            
            # Criar mapa de cores para cada comparação
            unique_comparisons = filtered_df["Comparison"].unique()
            color_idx = {comp: idx for idx, comp in enumerate(unique_comparisons)}
            color_palette = generate_distinct_colors(len(unique_comparisons))
            color_map = {comp: color_palette[color_idx[comp]] for comp in unique_comparisons}
            
            # Ajustar tamanho da figura com base no número de cromossomos
            fig_height = max(6, len(unique_chromosomes) * 0.8)
            fig, ax = plt.subplots(figsize=(12, fig_height))
            
            # Calcular posição Y para cada cromossomo com mais espaço
            chrom_height = 1.2  # Altura alocada para cada cromossomo
            y_positions = {chrom: idx * chrom_height for idx, chrom in enumerate(unique_chromosomes)}
            
            # Desenhar barras de cromossomos
            for chrom in unique_chromosomes:
                chrom_length = chromosome_sizes[chrom]
                chrom_data = filtered_df[filtered_df["Chr"] == chrom]
                
                # Posição base do cromossomo
                y_base = y_positions[chrom]
                
                # Desenhar barra de fundo do cromossomo
                ax.add_patch(plt.Rectangle((0, y_base - 0.3), chrom_length, 0.6, 
                                          color='lightgrey', alpha=0.3))
                
                # Agrupar segmentos por pessoa
                person_groups = chrom_data.groupby("Comparison")
                
                # Distribuir pessoas dentro do cromossomo
                num_persons = len(person_groups)
                person_height = 0.4 / max(1, num_persons)  # Altura do segmento por pessoa
                
                for i, (person, person_data) in enumerate(person_groups):
                    # Calcular posição Y para esta pessoa dentro do cromossomo
                    y_offset = y_base - 0.2 + (i * person_height)
                    
                    # Cor para esta pessoa
                    color = color_map[person]
                    
                    # Adicionar segmentos para esta pessoa
                    for _, row in person_data.iterrows():
                        segment_length = row["End"] - row["Start"]
                        ax.add_patch(plt.Rectangle(
                            (row["Start"], y_offset), 
                            segment_length, person_height, 
                            color=color, alpha=0.8
                        ))

            # Adiciona nome da comparação ao lado do segmento
    ax.text(
        row["End"] + max_chrom_size * 0.005,  # posicionamento ajustado para a direita do segmento
        y_offset + person_height / 2, 
        row["Comparison"],
        va='center', ha='left',
        fontsize=7,
        color='black'
    )
    
            # Configurar eixos
            # Definir limites do eixo X baseados no maior cromossomo sendo exibido
            max_chrom_size = max(chromosome_sizes[chrom] for chrom in unique_chromosomes)
ax.set_xlim(0, max_chrom_size * 1.05)  # 5% de margem
            
            # Ajustar limites do eixo Y para acomodar todos os cromossomos
            max_y = len(unique_chromosomes) * chrom_height
            ax.set_ylim(-0.5, max_y)
            
            # Posicionar rótulos do eixo Y no centro de cada cromossomo
            ax.set_yticks([y_positions[chrom] for chrom in unique_chromosomes])
            ax.set_yticklabels([f"Chr {chrom}" for chrom in unique_chromosomes])
            
            # Melhorar formatação do eixo X com números formatados
            from matplotlib.ticker import FuncFormatter
            ax.xaxis.set_major_formatter(FuncFormatter(format_x_ticks))
            
            # Adicionar título e rótulos
            ax.set_xlabel("Posição no Cromossomo (pb)")
            ax.set_title("Comparação de Múltiplos DNAs por Cromossomo")
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            
            # Salvar plot
            st.pyplot(fig)
            
            # Botão para baixar a imagem
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            img_bytes = buffer.getvalue()
            
            st.download_button(
                label="Baixar Imagem do Gráfico",
                data=img_bytes,
                file_name="chromosome_map.png",
                mime="image/png"
            )
            
            # Exibir legenda
            st.subheader("🔹 Legenda - Comparações")
            legend_cols = st.columns(min(4, len(color_map)))
            for i, (comp, color) in enumerate(color_map.items()):
                col_idx = i % len(legend_cols)
                color_hex = f'rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)})'
                legend_html = f"""
                <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                    <div style='width: 20px; height: 20px; background: {color_hex}; margin-right: 10px;'></div>
                    <div>{comp}</div>
                </div>
                """
                legend_cols[col_idx].markdown(legend_html, unsafe_allow_html=True)
            
            # Estatísticas
            st.subheader("📊 Estatísticas")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Total de segmentos", len(filtered_df))
            with stat_col2:
                st.metric("Cromossomos exibidos", len(unique_chromosomes))
            with stat_col3:
                st.metric("Pessoas comparadas", len(unique_comparisons))
            
            # Tabela detalhada por pessoa e cromossomo
            st.subheader("Detalhes por Pessoa e Cromossomo")
            
            # Adicionar colunas de tamanho e porcentagem
            analysis_df = filtered_df.copy()
            analysis_df["Segment_Size"] = analysis_df["End"] - analysis_df["Start"]
            
            # Agrupar por pessoa e cromossomo
            person_stats = analysis_df.groupby(["Comparison", "Chr"]).agg(
                Total_Segments=pd.NamedAgg(column="Chr", aggfunc="count"),
                Total_Size=pd.NamedAgg(column="Segment_Size", aggfunc="sum")
            ).reset_index()
            
            # Adicionar porcentagem do cromossomo
            person_stats["Chromosome_Size"] = person_stats["Chr"].map(chromosome_sizes)
            person_stats["Coverage_Percentage"] = (person_stats["Total_Size"] / person_stats["Chromosome_Size"] * 100).round(2)
            
            # Formatar os números
            person_stats["Formatted_Size"] = person_stats["Total_Size"].apply(format_number)
            person_stats["Formatted_Chr_Size"] = person_stats["Chromosome_Size"].apply(format_number)
            
            # Exibir tabela final
            display_df = person_stats[["Comparison", "Chr", "Total_Segments", "Formatted_Size", "Coverage_Percentage"]]
            display_df.columns = ["Pessoa", "Cromossomo", "Nº Segmentos", "Tamanho Total (pb)", "Cobertura (%)"]
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível após a aplicação dos filtros.")
    else:
        st.info("Nenhum dado disponível para visualização. Por favor, insira dados na aba 'Entrada de Dados'.")

with tab3:
    st.subheader("⚙️ Configurações da Aplicação")
    
    # Opção para editar tamanhos dos cromossomos
    st.write("Editar tamanhos dos cromossomos:")
    
    # Criar cópia modificável dos tamanhos
    if "custom_chrom_sizes" not in st.session_state:
        st.session_state.custom_chrom_sizes = chromosome_sizes.copy()
    
    # Interface para editar tamanhos
    cols_per_row = 3
    chrom_list = sorted(list(chromosome_sizes.keys()), key=lambda x: (isinstance(x, str), x))
    
    # Criar linhas de colunas
    for i in range(0, len(chrom_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(chrom_list):
                chrom = chrom_list[i + j]
                with cols[j]:
                    new_size = st.number_input(
                        f"Chr {chrom}",
                        min_value=1,
                        value=st.session_state.custom_chrom_sizes[chrom],
                        format="%d"
                    )
                    st.session_state.custom_chrom_sizes[chrom] = new_size
    
    # Botão para restaurar valores padrão
    if st.button("Restaurar tamanhos padrão"):
        st.session_state.custom_chrom_sizes = chromosome_sizes.copy()
        st.success("Tamanhos dos cromossomos restaurados para os valores padrão!")
    
    # Aplicar as alterações
    chromosome_sizes = st.session_state.custom_chrom_sizes
    
    # Informações adicionais
    st.write("---")
    st.info("Versão do aplicativo: 1.0.0")
    
    # Aviso sobre dependências
    if not EXCEL_AVAILABLE:
        st.warning("A biblioteca 'openpyxl' não está instalada. A exportação para Excel está desativada. Para habilitar esta funcionalidade, instale a biblioteca com 'pip install openpyxl'.")

