import os
import requests
import zipfile
from bs4 import BeautifulSoup
from tqdm import tqdm

# obtém o diretório onde o script está localizado
current_dir = os.path.dirname(os.path.abspath(__file__))

# URL da página e diretório para salvar os PDFs
site_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta_destino = os.path.join(current_dir, "anexos_ans")
os.makedirs(pasta_destino, exist_ok=True)

# requisição e parsing do HTML
resposta = requests.get(site_url)
soup_html = BeautifulSoup(resposta.text, "html.parser")

# lista para armazenar os links dos PDFs
lista_pdf = []

# coleta dos links de PDFs que contenham "Anexo I" ou "Anexo II" no título
for link in soup_html.find_all("a", href=True):
    titulo = link.get_text(strip=True)
    href_atual = link["href"]
    if (("Anexo I" in titulo or "Anexo II" in titulo) and href_atual.lower().endswith(".pdf")):
        lista_pdf.append(href_atual)

print(f"Foram identificados {len(lista_pdf)} arquivos PDF para download.")

# realiza o download dos PDFs
for endereco_pdf in tqdm(lista_pdf, desc="Baixando arquivos"):
    nome_arquivo = endereco_pdf.split("/")[-1]
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    
    resposta_pdf = requests.get(endereco_pdf, stream=True)
    with open(caminho_arquivo, "wb") as arquivo:
        for bloco in resposta_pdf.iter_content(chunk_size=1024):
            if bloco:
                arquivo.write(bloco)

print("Todos os downloads foram concluídos!")

# compacta os PDFs em um arquivo ZIP 
arquivo_zip = os.path.join(current_dir, "anexos_ans.zip")
with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zip_compactado:
    for raiz, _, arquivos in os.walk(pasta_destino):
        for arq in arquivos:
            zip_compactado.write(os.path.join(raiz, arq), arcname=arq)

print(f"Os arquivos foram compactados em: {arquivo_zip}")
