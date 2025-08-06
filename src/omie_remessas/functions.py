import requests
import json
import pandas as pd
import os


def incluir_remessa_omie(
    app_key: str,
    app_secret: str,
    cCodIntRem: str,
    dPrevisao: str,
    nCodCli: int,
    nCodRem: int,
    nCodVend: str,
    codigo_cenario_impostos: str,
    email_cEmail: str,
    frete_data: dict = None,
    agropecuario_data: dict = None,
    infAdic_data: dict = None,
    obs_cObs: str = None,
    produtos: list = None
) -> dict:
    """
    Inclui uma nova remessa na API da Omie.

    Args:
        app_key (str): Sua APP_KEY fornecida pela Omie.
        app_secret (str): Sua APP_SECRET fornecida pela Omie.
        cCodIntRem (str): Código de Integração da Remessa (identificador único).
        dPrevisao (str): Data de previsão da remessa (formato 'dd/mm/aaaa').
        nCodCli (int): Código do cliente no Omie.
        nCodRem (int): Código da remessa.
        nCodVend (str): Código do vendedor no Omie.
        codigo_cenario_impostos (str): Codigo cenario impostos no Omie.
        email_cEmail (str, optional): E-mail para notificação.
        frete_data (dict, optional): Dicionário com informações de frete.
        agropecuario_data (dict, optional): Dicionário com informações agropecuárias.
        infAdic_data (dict, optional): Dicionário com informações adicionais.
        obs_cObs (str, optional): Observações da remessa.
        produtos (list, optional): Lista de dicionários de produtos na remessa.

    Returns:
        dict: A resposta da API da Omie.
    """

    # URL do endpoint da API de Produtos/Remessa
    url = "https://app.omie.com.br/api/v1/produtos/remessa/"

    # Dados mínimos da remessa (cabecalho)
    cabecalho = {
        "cCodIntRem": cCodIntRem,
        "dPrevisao": dPrevisao,
        "nCodCli": nCodCli,
        "nCodRem": nCodRem,
        "nCodVend": nCodVend,
        "codigo_cenario_impostos": codigo_cenario_impostos
    }

    # Estrutura completa do payload (corpo da requisição)
    payload_param = {
        "cabec": cabecalho,
        "email": {"cEmail": email_cEmail} if email_cEmail else {},
        "frete": frete_data if frete_data else {},
        "agropecuario": agropecuario_data if agropecuario_data else {},
        "infAdic": infAdic_data if infAdic_data else {},
        "obs": {"cObs": obs_cObs} if obs_cObs else {},
        "produtos": produtos if produtos else []
    }

    # Estrutura completa da requisição Omie API
    request_body = {
        "call": "IncluirRemessa",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [payload_param]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(request_body), timeout=30)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx

        return response.json()

    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
        print(f"Resposta da API: {response.text}")
        return {"error": f"Erro HTTP: {errh}", "api_response": response.text}
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
        return {"error": f"Erro de Conexão: {errc}"}
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
        return {"error": f"Timeout: {errt}"}
    except requests.exceptions.RequestException as err:
        print(f"Erro na Requisição: {err}")
        return {"error": f"Erro na Requisição: {err}"}
    except json.JSONDecodeError as json_err:
        print(f"Erro ao decodificar JSON: {json_err}")
        print(f"Resposta bruta: {response.text}")
        return {"error": f"Erro ao decodificar JSON: {json_err}", "raw_response": response.text}

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------


import pandas as pd


def load_and_display_excel_from_request(file):
    """
    Lê dados de um arquivo Excel recebido via HTTP request (in-memory) e retorna como DataFrame.
    Compatível com FastAPI (UploadFile) e Flask (FileStorage).
    """
    filename = getattr(file, "filename", None) or getattr(file, "name", None)
    allowed_extensions = ('.xls', '.xlsx')

    if not (filename and filename.lower().endswith(allowed_extensions)):
        raise ValueError('O arquivo fornecido não é um arquivo Excel (.xls ou .xlsx).')

    try:
        # Se for UploadFile (FastAPI), file.file é o arquivo binário
        # Se for FileStorage (Flask), o próprio file é binário
        excel_stream = getattr(file, "file", file)
        data_table = pd.read_excel(excel_stream)

        # Opcional: debug para backend (não tente exibir em API real)
        # print(data_table.head())

        return data_table
    except Exception as e:
        raise Exception(f'Erro ao ler o arquivo Excel: {e}')