from src.omie_remessas.functions import incluir_remessa_omie, load_and_display_excel_from_request
from src.omie_remessas.dictionary import remessa_data

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import zipfile
import datetime
import os  # <--- para leitura da porta via variável de ambiente

app = FastAPI()

YOUR_APP_KEY = "923104076895"
YOUR_APP_SECRET = "caa5a11cfcf2881b1c55f90bedcaddcf"

@app.post("/processar_excel/")
async def processar_excel(file: UploadFile = File(...)):
    try:
        data_table = load_and_display_excel_from_request(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler o Excel: {e}")

    dados_remessas = []
    dados_erros = []

    sus_col = [c for c in data_table.columns if c.strip().lower().replace(' ', '') == 'cartãosus']
    sus_col = sus_col[0] if sus_col else None

    if not sus_col:
        return {"status": "Erro", "detalhe": "Coluna 'Cartão SUS' não encontrada no Excel."}

    for row_index in data_table.index:
        add_information_text = data_table.loc[row_index, 'DESCRIÇÃO NF COMPLETA']

        if pd.isna(add_information_text) or str(add_information_text).strip() == "":
            dados_erros.append({
                "tipo_erro": "AddInfo_vazio",
                "linha": row_index + 2,
                "cartao_sus": data_table.loc[row_index, sus_col],
            })
            continue

        remessa_data["cCodIntRem"] = f"REM-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        remessa_data["infAdic_data"]["cDadosAdic"] = add_information_text
        remessa_data["dPrevisao"] = datetime.datetime.now().strftime('%d/%m/%Y')

        resultado = incluir_remessa_omie(
            app_key=YOUR_APP_KEY,
            app_secret=YOUR_APP_SECRET,
            **remessa_data
        )

        nCodRem_resposta = resultado.get("nCodRem", None)
        nRem_omie_resposta = resultado.get("cNumeroRemessa", None)

        if resultado and resultado.get("cDesStatus") == "Remessa de Produto cadastrada com sucesso!":
            dados_remessas.append({
                "cCodIntRem": remessa_data["cCodIntRem"],
                "descricao_nf": add_information_text,
                "nCodRem": nCodRem_resposta,
                "cNumeroRemessa": nRem_omie_resposta,
                "status": resultado.get("cDesStatus", None)
            })
        else:
            dados_erros.append({
                "tipo_erro": "Status_NF",
                "linha": row_index + 2,
                "cartao_sus": data_table.loc[row_index, sus_col],
                "status": resultado.get("cDesStatus", ""),
                "mensagem": resultado.get("error", "")
            })

    # SEMPRE cria os DataFrames para poder gerar os arquivos, mesmo vazios.
    df_remessas = pd.DataFrame(dados_remessas)
    df_erros = pd.DataFrame(dados_erros)

    # Gera arquivos Excel em memória
    remessas_buffer = io.BytesIO()
    erros_buffer = io.BytesIO()

    with pd.ExcelWriter(remessas_buffer, engine='xlsxwriter') as writer:
        df_remessas.to_excel(writer, index=False)
    remessas_buffer.seek(0)

    with pd.ExcelWriter(erros_buffer, engine='xlsxwriter') as writer:
        df_erros.to_excel(writer, index=False)
    erros_buffer.seek(0)

    # Cria ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("remessas_processadas.xlsx", remessas_buffer.read())
        zip_file.writestr("remessas_com_erro.xlsx", erros_buffer.read())
    zip_buffer.seek(0)

    # Responde o ZIP ao n8n
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": 'attachment; filename="resultado_planilhas.zip"'
        }
    )

# --- Bloco para rodar o app com porta configurável ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Usa a variável de ambiente PORT, ou padrão 8000
    uvicorn.run("src.omie_remessas.main:app", host="0.0.0.0", port=port, reload=True)