# Use uma imagem base oficial do Python
FROM python:3.11-slim-bullseye

# Define o ambiente como não-interativo para evitar prompts durante apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# --- Adiciona dependências de sistema e ferramentas de compilação ---
# Atualiza a lista de pacotes e instala as dependências comuns para pacotes Python.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        dpkg-dev \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        netcat \
        libatlas-base-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do seu diretório src (onde está o main.py e outras pastas)
# para o diretório de trabalho dentro do contêiner.
# NOTA: O 'WORKDIR /app' já garante que o . é o /app.
# Se seu diretório local 'src' contém a pasta 'omie_remessas',
# então o caminho dentro do container será /app/src/omie_remessas.
COPY src /app/src

# Remove a necessidade de `ENV PYTHONPATH=/app/src` se você usar `python -m`
# porque `WORKDIR /app` e `python -m src.omie_remessas.main` já cuidam do caminho.
# Porém, manter pode não fazer mal, mas não é estritamente necessário neste caso.
# ENV PYTHONPATH=/app/src # Pode ser removido, mas não é obrigatório

# Comando para executar seu aplicativo quando o contêiner iniciar
# MUDANÇA ESSENCIAL AQUI: Usando -m para executar o módulo como parte do pacote
CMD ["python", "-m", "src.omie_remessas.main"]

# Se sua aplicação for uma API web e escutar em uma porta, você deve expô-la.
# Por exemplo, se sua API rodar na porta 8000, descomente a linha abaixo:
# EXPOSE 8000