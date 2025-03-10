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

# Configuração inicial do Streamlit
st.title("🔬 Visualizador de Mapa Cromossômico - Comparação de Múltiplos DNAs")

# 
