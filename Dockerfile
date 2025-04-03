# Imagem base com Python
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Expõe a porta que seu servidor utiliza (ex: 5000)
EXPOSE 5000

# Comando para iniciar o servidor
CMD ["python", "api/app.py"]