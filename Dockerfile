# Use uma imagem base oficial do Python
# Recomenda-se usar uma versão específica, por exemplo, python:3.9-slim-buster
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
# Todos os comandos subsequentes serão executados a partir deste diretório
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt
# A opção --no-cache-dir é para economizar espaço na imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do seu diretório src (onde está o main.py e outras pastas)
# para o diretório de trabalho dentro do contêiner.
# Assumimos que 'src' é a pasta que contém o código do seu aplicativo.
COPY src /app/src

# Define a variável de ambiente para que o Python encontre os módulos do seu app
# Isso adiciona o diretório src ao PYTHONPATH, permitindo importações como 'from omie_remessas import main'
ENV PYTHONPATH=/app/src

# Comando para executar seu aplicativo quando o contêiner iniciar
# Este comando assume que seu ponto de entrada é `main.py` dentro da pasta `omie_remessas`
# Certifique-se de que `main.py` seja o script principal que você quer que rode.
# Se seu main.py está em src/omie_remessas/main.py, este é o caminho correto relativo a PYTHONPATH.
CMD ["python", "src/omie_remessas/main.py"]

# Se sua aplicação for uma API web e escutar em uma porta, você deve expô-la.
# Por exemplo, se sua API rodar na porta 8000, descomente a linha abaixo:
# EXPOSE 8000