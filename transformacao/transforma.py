import pdfplumber
import pandas as pd
import os
import zipfile

# define os diretórios
projeto_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
anexos_dir = os.path.join(projeto_dir, "web_scraping", "anexos_ans")
transformacao_dir = os.path.join(projeto_dir, "transformacao")

# localiza o arquivo PDF Anexo I
pdf_files = [f for f in os.listdir(anexos_dir) if f.startswith("Anexo_I_") and f.lower().endswith(".pdf")]
if not pdf_files:
    raise FileNotFoundError("Nenhum arquivo Anexo I encontrado na pasta anexos_ans.")
pdf_path = os.path.join(anexos_dir, pdf_files[0])
print(f"Utilizando o arquivo PDF: {pdf_path}")

# lista para armazenar os dados extraídos
dados = []

# lê e processa o PDF
with pdfplumber.open(pdf_path) as pdf:
    for pagina in pdf.pages[2:181]:
        tabela = pagina.extract_table()
        if tabela:
            dados.extend(tabela)

# verifica se as linhas foram extraídas
if not dados:
    raise ValueError("Nenhuma tabela foi extraída do PDF.")

# assume que a primeira linha extraída seja o cabeçalho
cabecalho = dados[0]

# defina as colunas esperadas
colunas_esperadas = [
    "PROCEDIMENTO", "RN(Alteração)", "Vigência", "OD", "AMB",
    "HCO", "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPÍTULO"
]

# cria o DataFrame ignorando as linhas de cabeçalho repetidas
linhas = []
for linha in dados:
    if linha == cabecalho:
        continue
    linhas.append(linha)

df = pd.DataFrame(linhas, columns=cabecalho)

# caso alguma linha esteja quebrada mescla a linha com a anterior
linhas_mescladas = []
acumulada = None
for idx, row in df.iterrows():
    valor_proc = str(row["PROCEDIMENTO"]).strip()
    if valor_proc == "":
        if acumulada is not None:
            for col in colunas_esperadas:
                conteudo = str(row[col]).strip()
                if conteudo:
                    acumulada[col] = str(acumulada[col]).strip() + " " + conteudo
    else:
        if acumulada is not None:
            linhas_mescladas.append(acumulada)
        acumulada = row.copy()
if acumulada is not None:
    linhas_mescladas.append(acumulada)

df_final = pd.DataFrame(linhas_mescladas)
df_final.reset_index(drop=True, inplace=True)

# substitui as abreviações conforme a legenda
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}
df_final = df_final.replace(substituicoes)

# salva o CSV 
csv_path = os.path.join(transformacao_dir, "dados_transformados.csv")
df_final.to_csv(csv_path, index=False, encoding="utf-8")

print(f"CSV salvo em: {csv_path}")

# compacta o CSV em um arquivo ZIP
zip_filename = os.path.join(transformacao_dir, "Teste_BeatrizLimaCardoso.zip")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path, arcname="dados_transformados.csv")

print(f"O arquivo foi compactado em: {zip_filename}")
