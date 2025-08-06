remessa_data = {
    # ----------------- CABEÇALHO (OBRIGATÓRIO) -----------------
    "cCodIntRem": "",  # Código único identificado da remessa (personalizado por você)
    "dPrevisao": "",  # Data da previsão/envio da remessa (formato dia/mês/ano)
    "nCodCli": '1171304297',  # Código do Cliente no sistema Omie (obrigatório)
    "nCodRem": 0,  # Código da remessa: 0 para inclusão (novo registro), código específico para alteração
    "nCodVend": None,  # Código do vendedor responsável (opcional)
    "codigo_cenario_impostos": None,  # Cenário de impostos definido no Omie (opcional)

    # ----------------- EMAIL (OPCIONAL) -----------------
    "email_cEmail": "gbrito@prefeitura.sp.gov.br",  # Email de contato do cliente ou responsável pela remessa

    # ----------------- FRETE (OPCIONAL) -----------------
    "frete_data": {
        "cEspVol": "caixa",  # Tipo de embalagem ou volume (ex: caixa, pacote, etc.)
        "cMarVol": None,  # Marca do volume (opcional)
        "cNumVol": None,  # Número do volume (opcional)
        "cPlaca": None,  # Placa do veículo de transporte (opcional)
        "cTpFrete": 0,  # Tipo de frete: 0 = CIF, 1 = FOB, etc.
        "cUF": None,  # Unidade federativa da placa (opcional)
        "nCodTransp": None,  # Código do transportador no Omie (opcional)
        "nPesoBruto": 0.000,  # Peso bruto da remessa em kg
        "nPesoLiq": 20.000,  # Peso líquido da remessa em kg
        "nQtdVol": 2,  # Quantidade de volumes
        "nValFrete": 0.000,  # Valor do frete (opcional)
        "nValOutras": 0.000,  # Outros valores (opcional)
        "nValSeguro": 0.000  # Valor do seguro (opcional)
    },

    # ----------------- AGROPECUÁRIO (OPCIONAL) -----------------
    "agropecuario_data": {
        "cNumReceita": None,  # Número de receita (se pertinente)
        "cCpfResponsavel": None,  # CPF do responsável (se pertinente)
        "nTipoGuia": None,  # Tipo de guia agropecuária (opcional)
        "cUFGuia": None,  # Estado da guia (opcional)
        "cSerieGuia": None,  # Série da guia (opcional)
        "nNumGuia": None  # Número da guia (opcional)
    },

    # ----------- INFORMAÇÕES ADICIONAIS (OPCIONAL) -------------
    "infAdic_data": {
        "cCodCateg": '1.01.03',  # Código de categoria (personalizado)
        "cConsFinal": "S",  # Consumidor final: "S" (Sim), "N" (Não)
        "cContato": None,  # Nome do contato (opcional)
        "cDadosAdic": "",  # Informações adicionais (pode ser uma string com instruções, referência, etc.)
        "cNumCtr": None,  # Número do contrato (opcional)
        "cPedido": None,  # Número do pedido (opcional)
        "nCodProj": None  # Código do projeto (opcional)
    },

    # ----------------- OBSERVAÇÕES (OPCIONAL) -----------------
    "obs_cObs": "REMESSA TESTE",  # Observação livre sobre a remessa

    # ----------- PRODUTOS (LISTA, OBRIGATÓRIO SE HOUVER) -------------
    "produtos": [
        {
            "cCodItInt": "6000073-152",  # Código interno (SKU) do produto
            "nCodIt": 0,  # 0 para adicionar novo item à remessa
            "nCodProd": 1474360332,  # Código do produto cadastrado no Omie (obrigatório)
            "nQtde": 30.0,  # Quantidade do produto na remessa
            "nValUnit": 1.0,  # Valor unitário do produto
            "cCFOP": "5.949",  # CFOP: Código Fiscal de Operações e Prestações

            # --- IMPOSTOS (OBRIGATÓRIO OU OPCIONAL, CONFORME REGIME) ---
            "ICMS": {
                "cSitTrib": "41",  # Situação tributária do ICMS
                "cOrigem": "0",  # Origem do produto (0 = nacional)
                "nAliq": 0.00  # Alíquota do ICMS
            },
            "IPI": {
                "cSitTribIPI": "53",  # Situação tributária do IPI
                "cEnqIPI": "999"  # Enquadramento do IPI
            },
            "PIS": {
                "cSitTribPIS": "49",  # Situação tributária do PIS
                "cTpCalcPIS": "B"  # Tipo de cálculo do PIS (ex: "B" = base de cálculo)
            },
            "COFINS": {
                "cSitTribCOFINS": "49",  # Situação tributária do COFINS
                "cTpCalcCOFINS": "B"  # Tipo de cálculo do COFINS (ex: "B" = base de cálculo)
            }
        }
    ]
}