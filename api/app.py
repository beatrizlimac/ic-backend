from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)

# configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql:3306/ans_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicializa o banco de dados
db = SQLAlchemy(app)

# modelo da tabela operadoras_ativas
class OperadoraAtiva(db.Model):
    __tablename__ = 'operadoras_ativas'
    id_operadoras = db.Column(db.Integer, primary_key=True)
    registro_ans = db.Column(db.String(20))
    cnpj = db.Column(db.String(20))
    razao_social = db.Column(db.String(355))
    nome_fantasia = db.Column(db.String(255))
    modalidade = db.Column(db.String(100))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(15))
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(5))
    cep = db.Column(db.String(10))
    ddd = db.Column(db.String(5))
    telefone = db.Column(db.String(25))
    fax = db.Column(db.String(15))
    endereco_eletronico = db.Column(db.String(255))
    representante = db.Column(db.String(255))
    cargo_representante = db.Column(db.String(255))
    regiao_da_comercializacao = db.Column(db.String(10))

@app.route('/')
# Rota inicial
def home():
    
    termo = request.args.get('q', '').strip()
    if not termo:
        return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400
  
    resultados = OperadoraAtiva.query.filter(
        or_(
            OperadoraAtiva.registro_ans.ilike(f'%{termo}%'),
            OperadoraAtiva.cnpj.ilike(f'%{termo}%'),
            OperadoraAtiva.razao_social.ilike(f'%{termo}%'),
            OperadoraAtiva.nome_fantasia.ilike(f'%{termo}%'),
            OperadoraAtiva.modalidade.ilike(f'%{termo}%'),
            OperadoraAtiva.logradouro.ilike(f'%{termo}%'),
            OperadoraAtiva.numero.ilike(f'%{termo}%'),
            OperadoraAtiva.complemento.ilike(f'%{termo}%'),
            OperadoraAtiva.bairro.ilike(f'%{termo}%'),
            OperadoraAtiva.cidade.ilike(f'%{termo}%'),
            OperadoraAtiva.uf.ilike(f'%{termo}%'),
            OperadoraAtiva.cep.ilike(f'%{termo}%'),
            OperadoraAtiva.ddd.ilike(f'%{termo}%'),
            OperadoraAtiva.telefone.ilike(f'%{termo}%'),
            OperadoraAtiva.fax.ilike(f'%{termo}%'),
            OperadoraAtiva.endereco_eletronico.ilike(f'%{termo}%'),
            OperadoraAtiva.representante.ilike(f'%{termo}%'),
            OperadoraAtiva.cargo_representante.ilike(f'%{termo}%'),
            OperadoraAtiva.regiao_da_comercializacao.ilike(f'%{termo}%'),
            
        )
    ).all()

    output = []
    for op in resultados:
        output.append({
            "registro_ans": op.registro_ans,
            "cnpj": op.cnpj,
            "razao_social": op.razao_social,
            "nome_fantasia": op.nome_fantasia,
            "modalidade": op.modalidade,
            "logradouro": op.logradouro,
            "numero": op.numero,
            "complemento": op.complemento,
            "bairro": op.bairro,
            "cidade": op.cidade,
            "uf": op.uf,
            "cep": op.cep,
            "ddd": op.ddd,
            "telefone": op.telefone,
            "fax": op.fax,
            "endereco_eletronico": op.endereco_eletronico,
            "representante": op.representante,
            "cargo_representante": op.cargo_representante,
            "regiao_da_comercializacao": op.regiao_da_comercializacao,
            "data_registro_ans": op.data_registro_ans.strftime('%Y-%m-%d') if op.data_registro_ans else None
        })

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
