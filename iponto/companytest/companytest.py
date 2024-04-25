from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iponto.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'secreto'

jwt = JWTManager(app)

# Definindo modelos
# class Company(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     cnpj = db.Column(db.String(255), nullable=False, unique=True)
#     lat = db.Column(db.Float)
#     lng = db.Column(db.Float)

# Endpoint para criar uma nova empresa
@app.route('/api/v1/company/', methods=['POST'])
@jwt_required()
def criar_empresa():
    data = request.json
    name = data.get('name')
    cnpj = data.get('cnpj')
    lat = data.get('lat')
    lng = data.get('lng')

    if not name:
        return jsonify({'error': 'O campo name é obrigatório'}), 400

    existing_company = Company.query.filter_by(cnpj=cnpj).first()
    if existing_company:
        return jsonify({'error': 'Já existe uma empresa com este CNPJ'}), 400

    nova_empresa = Company(name=name, cnpj=cnpj, lat=lat, lng=lng)
    db.session.add(nova_empresa)
    db.session.commit()

    return jsonify({'id': nova_empresa.id}), 200

# Endpoint para criar um novo funcionário
@app.route('/api/v1/employee/', methods=['POST'])
@jwt_required()
def criar_funcionario():
    data = request.json
    name = data.get('name')
    role_id = data.get('role_id')
    document = data.get('document')
    company_id = data.get('company_id')

    if not name:
        return jsonify({'error': 'O campo name é obrigatório'}), 400

    existing_employee = Employee.query.filter_by(document=document).first()
    if existing_employee:
        return jsonify({'error': 'Já existe um funcionário com este documento'}), 400

    if not Company.query.get(company_id):
        return jsonify({'error': 'Não existe essa empresa no sistema'}), 400

    novo_funcionario = Employee(name=name, role_id=role_id, document=document, company_id=company_id)
    db.session.add(novo_funcionario)
    db.session.commit()

    return jsonify({'id': novo_funcionario.id}), 200

# Endpoint para editar um funcionário existente
@app.route('/api/v1/employee/<int:id>/', methods=['PUT'])
@jwt_required()
def editar_funcionario(id):

    data = request.json
    name = data.get('name')
    role_id = data.get('role_id')
    document = data.get('document')
    company_id = data.get('company_id')

    if not name:
        return jsonify({'error': 'O campo name é obrigatório'}), 400

    funcionario = Employee.query.get(id)
    if not funcionario:
        return jsonify({'error': 'Funcionário não encontrado'}), 400

    funcionario.name = name
    funcionario.role_id = role_id
    funcionario.document = document
    funcionario.company_id = company_id
    db.session.commit()

    return jsonify({'id': funcionario.id}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
