import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Validador de Planilhas Nibo", layout="wide")
st.title("🔢 Validador de Planilhas de Importação - Nibo")

# Upload dos arquivos
template_file = st.sidebar.file_uploader("Template oficial do Nibo", type="xlsx")
user_file = st.sidebar.file_uploader("Planilha a ser validada", type="xlsx")

if template_file and user_file:
    # Leitura dos arquivos
    template_df = pd.read_excel(template_file)
    user_df = pd.read_excel(user_file)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Colunas obrigatórias")

    # Permitir ao usuário escolher colunas obrigatórias com base nas colunas do template
    selected_columns = st.sidebar.multiselect(
        "Selecione as colunas que devem ser obrigatórias:",
        options=template_df.columns.tolist(),
        default=[col for col in template_df.columns if col in ["Valor", "Vencimento"]]
    )

    # Lista de erros
    erros = []

    for idx, row in user_df.iterrows():
        linha = idx + 2  # considerando cabeçalho na linha 1

        for col in selected_columns:
            if col in row and pd.isnull(row[col]):
                erros.append({"Linha": linha, "Coluna": col, "Erro": "Campo obrigatório ausente"})

            # Valida datas se for coluna de data
            if col.lower() in ["vencimento", "previsto para", "competência", "data pag/rec/transferência"]:
                try:
                    pd.to_datetime(row[col], dayfirst=True)
                except:
                    erros.append({"Linha": linha, "Coluna": col, "Erro": "Data inválida"})

        # Linha totalmente vazia
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

