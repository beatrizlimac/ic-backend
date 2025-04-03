## Repositório
__ic-backend:__  
- __Descrição:__
Contém a API Python (desenvolvida com Flask) que expõe uma rota para realizar a busca textual na lista de cadastros de operadoras.
Também inclui dois scripts auxiliares:

   - `transforma.py:` Script para transformação de dados (por exemplo, extração e formatação de informações do PDF do rol de procedimentos).

   - `scraping.py:` Script para realizar web scraping, acessando o site da ANS e efetuando o download dos anexos indicados.
       
- __Containerização:__
Possui um Dockerfile que constrói a imagem Docker do backend.
