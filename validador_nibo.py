import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Validador de Planilhas Nibo", layout="wide")
st.title("🔢 Validador de Planilhas de Importação - Nibo")

# Upload do arquivo de exemplo (template)
st.sidebar.header("📁 Enviar arquivos")
template_file = st.sidebar.file_uploader("Template oficial do Nibo", type="xlsx")
user_file = st.sidebar.file_uploader("Planilha a ser validada", type="xlsx")

if template_file and user_file:
    # Leitura dos arquivos
    template_df = pd.read_excel(template_file)
    user_df = pd.read_excel(user_file)

    # Lista de erros
    erros = []

    for idx, row in user_df.iterrows():
        linha = idx + 2  # considerando cabeçalho na linha 1

        # Verifica colunas obrigatórias
        if 'Valor' in row and pd.isnull(row['Valor']):
            erros.append({"Linha": linha, "Coluna": "Valor", "Erro": "Campo obrigatório ausente"})

        if 'Vencimento' in row:
            try:
                pd.to_datetime(row['Vencimento'], dayfirst=True)
            except:
                erros.append({"Linha": linha, "Coluna": "Vencimento", "Erro": "Data inválida"})

        if 'Referência' in row and pd.isnull(row['Referência']):
            erros.append({"Linha": linha, "Coluna": "Referência", "Erro": "Campo obrigatório ausente"})

        if row.isnull().all():
            erros.append({"Linha": linha, "Coluna": "-", "Erro": "Linha completamente vazia"})

    if erros:
        st.subheader(":warning: Erros encontrados")
        erro_df = pd.DataFrame(erros)
        st.dataframe(erro_df)

        # Gerar arquivo de erros para download
        output = BytesIO()
        erro_df.to_excel(output, index=False)
        st.download_button("📄 Baixar relatório de erros", output.getvalue(), file_name="erros_validacao.xlsx")
    else:
        st.success("✅ Nenhum erro encontrado. Planilha pronta para importação!")

else:
    st.info("⬆️ Envie os arquivos para iniciar a validação.")
