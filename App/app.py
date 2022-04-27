from flask import Flask, abort, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/imobiliaria'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Aluguel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_corretor = db.Column(db.Integer, db.ForeignKey('corretor.id'))
    id_imovel = db.Column(db.Integer, db.ForeignKey('imovel.id'))
    id_contrato = db.Column(db.Integer, db.ForeignKey('contrato.id'))
    id_inquilino = db.Column(db.Integer, db.ForeignKey('inquilino.id'))
    valor = db.Column(db.Float(), nullable=False)
    exige_calcao = db.Column(db.String(), nullable=False)
    aceita_melhorias = db.Column(db.String(), nullable=False)

    def __init__(self, id_corretor, id_imovel, id_contrato, id_inquilino, valor, exige_calcao, aceita_melhorias):
        self.id_corretor = id_corretor
        self.id_imovel = id_imovel
        self.id_contrato = id_contrato
        self.id_inquilino = id_inquilino
        self.valor = valor
        self.exige_calcao = exige_calcao
        self.aceita_melhorias = aceita_melhorias


class Proprietario(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    sobrenome = db.Column(db.String(), nullable=False)
    endereco = db.Column(db.String(), nullable=False)
    cpf = db.Column(db.String(), nullable=False)
    data_nascimento = db.Column(db.Date(), nullable=False)
    telefone = db.Column(db.String())

    def __init__(self, nome, sobrenome, endereco, cpf, data_nascimento, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.endereco = endereco
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone


class Inquilino(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    sobrenome = db.Column(db.String(), nullable=False)
    cpf = db.Column(db.String(), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date(), nullable=False)
    telefone = db.Column(db.String())

    def __init__(self, nome, sobrenome, cpf, data_nascimento, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone


class Corretor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    sobrenome = db.Column(db.String(), nullable=False)
    endereco = db.Column(db.String(), nullable=False)
    cpf = db.Column(db.String(), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date(), nullable=False)
    telefone = db.Column(db.String())

    def __init__(self, nome, sobrenome, endereco, cpf, data_nascimento, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.endereco = endereco
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone


class Imovel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_proprietario = db.Column(db.Integer, db.ForeignKey('proprietario.id'))
    tipo_imovel = db.Column(db.String(), nullable=False)
    endereco = db.Column(db.String(), unique=True, nullable=False)
    garagem_propria = db.Column(db.String(), nullable=False)
    metragem = db.Column(db.Float(), nullable=False)
    num_salas = db.Column(db.Integer(), nullable=False)
    num_banheiros = db.Column(db.Integer(), nullable=False)
    num_vagas = db.Column(db.Integer(), nullable=False)
    num_elevadores = db.Column(db.Integer(), nullable=False)
    escada_incendio = db.Column(db.String(), nullable=False)
    tipo_recepcao = db.Column(db.String(), nullable=False)

    def __init__(self, id_proprietario, tipo_imovel, endereco, garagem_propria, metragem, num_salas, num_banheiros, num_vagas, num_elevadores, escada_incendio, tipo_recepcao):
        self.id_proprietario = id_proprietario
        self.tipo_imovel = tipo_imovel
        self.endereco = endereco
        self.garagem_propria = garagem_propria
        self.metragem = metragem
        self.num_salas = num_salas
        self.num_banheiros = num_banheiros
        self.num_vagas = num_vagas
        self.num_elevadores = num_elevadores
        self.escada_incendio = escada_incendio
        self.tipo_recepcao = tipo_recepcao


class Contrato(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tipo_contrato = db.Column(db.String(), nullable=False)
    fiador = db.Column(db.String(), nullable=False)
    data_inicio = db.Column(db.Date(), nullable=False)
    data_fim = db.Column(db.Date(), nullable=False)

    def __init__(self, tipo_contrato, fiador, data_inicio, data_fim):
        self.tipo_contrato = tipo_contrato
        self.fiador = fiador
        self.data_inicio = data_inicio
        self.data_fim = data_fim


@app.route('/')
def index():
    return render_template('index.html')


# Rotas Show all
@app.route('/show_all_inquilinos')
def show_all_inquilinos():
    return render_template('show_all_inquilinos.html', inquilino=Inquilino.query.all())


@app.route('/show_all_proprietarios')
def show_all_proprietarios():
    return render_template('show_all_proprietarios.html', proprietario=Proprietario.query.all())


@app.route('/show_all_corretores')
def show_all_corretores():
    return render_template('show_all_corretores.html', corretores=Corretor.query.all())


@app.route('/show_all_imoveis')
def show_all_imoveis():
    return render_template('show_all_imoveis.html', imovel=Imovel.query.all(), proprietario=Proprietario.query.all())


@app.route('/show_all_contratos')
def show_all_contratos():
    return render_template('show_all_contratos.html', contrato=Contrato.query.all())


@app.route('/show_all_alugueis')
def show_all_alugueis():
    return render_template('show_all_alugueis.html', aluguel=Aluguel.query.all(), corretor=Corretor.query.all(), imovel=Imovel.query.all(), contrato=Contrato.query.all(), inquilino=Inquilino.query.all())


# Rotas novos
@app.route('/new_inquilino', methods=['GET', 'POST'])
def new_inquilino():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['sobrenome'] or not request.form['data_nascimento'] or not request.form['cpf'] or not request.form['telefone']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            inquilino = Inquilino(request.form['nome'], request.form['sobrenome'],
                                  request.form['cpf'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(inquilino)
            db.session.commit()
            flash('Inquilino cadastrado com sucesso')
            return redirect(url_for('show_all_inquilinos'))
    return render_template('new_inquilino.html')


@app.route('/new_proprietario', methods=['GET', 'POST'])
def new_proprietario():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['sobrenome'] or not request.form['endereco'] or not request.form['data_nascimento'] or not request.form['cpf'] or not request.form['telefone']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            proprietario = Proprietario(request.form['nome'], request.form['sobrenome'], request.form['endereco'],
                                        request.form['cpf'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(proprietario)
            db.session.commit()
            flash('Proprietário cadastrado com sucesso')
            return redirect(url_for('show_all_proprietarios'))
    return render_template('new_proprietario.html')


@app.route('/new_corretor', methods=['GET', 'POST'])
def new_corretor():

    if request.method == 'POST':
        if not request.form['nome'] or not request.form['sobrenome'] or not request.form['endereco'] or not request.form['data_nascimento'] or not request.form['cpf'] or not request.form['telefone']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            corretor = Corretor(request.form['nome'], request.form['sobrenome'], request.form['endereco'],
                                request.form['cpf'], request.form['data_nascimento'], request.form['telefone'])

            db.session.add(corretor)
            db.session.commit()
            flash('Corretor cadastrado com sucesso')
            return redirect(url_for('show_all_corretores'))
    return render_template('new_corretor.html')


@app.route('/new_imovel', methods=['GET', 'POST'])
def new_imovel():
    proprietario = Proprietario.query.all()

    if request.method == 'POST':
        if not request.form['id_proprietario'] or not request.form['tipo_imovel'] or not request.form['endereco'] or not request.form['garagem_propria'] or not request.form['metragem'] or not request.form['num_salas'] or not request.form['num_banheiros'] or not request.form['num_vagas'] or not request.form['num_elevadores'] or not request.form['escada_incendio'] or not request.form['tipo_recepcao']:

            flash('Por favor preencha todos os campos', 'error')
        else:
            imovel = Imovel(request.form['id_proprietario'], request.form['tipo_imovel'], request.form['endereco'], request.form['garagem_propria'], request.form['metragem'],
                            request.form['num_salas'], request.form['num_banheiros'], request.form['num_vagas'], request.form['num_elevadores'], request.form['escada_incendio'], request.form['tipo_recepcao'])

            db.session.add(imovel)
            db.session.commit()
            flash('Imóvel cadastrado com sucesso')
            return redirect(url_for('show_all_imoveis'))
    return render_template('new_imovel.html', proprietario=proprietario)


@app.route('/new_contrato', methods=['GET', 'POST'])
def new_contrato():

    if request.method == 'POST':
        if not request.form['tipo_contrato'] or not request.form['fiador'] or not request.form['data_inicio'] or not request.form['data_fim']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            contrato = Contrato(request.form['tipo_contrato'], request.form['fiador'],
                                request.form['data_inicio'], request.form['data_fim'])

            db.session.add(contrato)
            db.session.commit()
            flash('Contrato cadastrado com sucesso')
            return redirect(url_for('show_all_contratos'))
    return render_template('new_contrato.html')


@app.route('/new_aluguel', methods=['GET', 'POST'])
def new_aluguel():
    corretor = Corretor.query.all()
    imovel = Imovel.query.all()
    contrato = Contrato.query.all()
    inquilino = Inquilino.query.all()

    if request.method == 'POST':
        if not request.form['id_corretor'] or not request.form['id_imovel'] or not request.form['id_contrato'] or not request.form['id_inquilino'] or not request.form['valor'] or not request.form['exige_calcao'] or not request.form['aceita_melhorias']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            aluguel = Aluguel(request.form['id_corretor'], request.form['id_imovel'], request.form['id_contrato'],
                              request.form['id_inquilino'], request.form['valor'], request.form['exige_calcao'], request.form['aceita_melhorias'])

            db.session.add(aluguel)
            db.session.commit()
            flash('Aluguel cadastrado com sucesso')
            return redirect(url_for('show_all_alugueis'))
    return render_template('new_aluguel.html', corretor=corretor, imovel=imovel, contrato=contrato, inquilino=inquilino)


# Rotas update
@app.route('/inquilino/<id>', methods=['GET', 'POST'])
def update_inquilino(id):
    inquilino = Inquilino.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('update_inquilino.html', inquilino=inquilino)

    if request.method == 'POST':
        inquilino.nome = request.form["nome"]
        inquilino.sobrenome = request.form["sobrenome"]
        inquilino.cpf = request.form["cpf"]
        inquilino.data_nascimento = request.form["data_nascimento"]
        inquilino.telefone = request.form["telefone"]

        db.session.add(inquilino)
        db.session.commit()

        flash('Inquilino atualizado com sucesso')
        return redirect(url_for('show_all_inquilinos'))


@app.route('/proprietario/<id>', methods=['GET', 'POST'])
def update_proprietario(id):
    proprietario = Proprietario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('update_proprietario.html', proprietario=proprietario)

    if request.method == 'POST':
        proprietario.nome = request.form["nome"]
        proprietario.sobrenome = request.form["sobrenome"]
        proprietario.endereco = request.form["endereco"]
        proprietario.cpf = request.form["cpf"]
        proprietario.data_nascimento = request.form["data_nascimento"]
        proprietario.telefone = request.form["telefone"]

        db.session.add(proprietario)
        db.session.commit()

        flash('Proprietario atualizado com sucesso')
        return redirect(url_for('show_all_proprietarios'))


@app.route('/corretor/<id>', methods=['GET', 'POST'])
def update_corretor(id):
    corretor = Corretor.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('update_corretor.html', corretor=corretor)

    if request.method == 'POST':
        corretor.nome = request.form["nome"]
        corretor.sobrenome = request.form["sobrenome"]
        corretor.endereco = request.form["endereco"]
        corretor.cpf = request.form["cpf"]
        corretor.data_nascimento = request.form["data_nascimento"]
        corretor.telefone = request.form["telefone"]

        db.session.add(corretor)
        db.session.commit()

        flash('Corretor atualizado com sucesso')
        return redirect(url_for('show_all_corretores'))


@app.route('/imovel/<id>', methods=['GET', 'POST'])
def update_imovel(id):
    imovel = Imovel.query.get_or_404(id)
    proprietario = Proprietario.query.all()

    if request.method == 'GET':
        return render_template('update_imovel.html', imovel=imovel, proprietario=proprietario)

    if request.method == 'POST':
        imovel.id_proprietario = request.form["id_proprietario"]
        imovel.tipo_imovel = request.form["tipo_imovel"]
        imovel.endereco = request.form["endereco"]
        imovel.garagem_propria = request.form["garagem_propria"]
        imovel.metragem = request.form["metragem"]
        imovel.num_salas = request.form["num_salas"]
        imovel.num_banheiros = request.form["num_banheiros"]
        imovel.num_vagas = request.form["num_vagas"]
        imovel.num_elevadores = request.form["num_elevadores"]
        imovel.escada_incendio = request.form["escada_incendio"]
        imovel.tipo_recepcao = request.form["tipo_recepcao"]

        db.session.add(imovel)
        db.session.commit()

        flash('Imovel atualizado com sucesso')
        return redirect(url_for('show_all_imoveis'))


@app.route('/contrato/<id>', methods=['GET', 'POST'])
def update_contrato(id):
    contrato = Contrato.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('update_contrato.html', contrato=contrato)

    if request.method == 'POST':
        contrato.tipo_contrato = request.form["tipo_contrato"]
        contrato.fiador = request.form["fiador"]
        contrato.data_inicio = request.form["data_inicio"]
        contrato.data_fim = request.form["data_fim"]

        db.session.add(contrato)
        db.session.commit()

        flash('Contrato atualizado com sucesso')
        return redirect(url_for('show_all_contratos'))


@app.route('/aluguel/<id>', methods=['GET', 'POST'])
def update_aluguel(id):
    aluguel = Aluguel.query.get_or_404(id)
    inquilino = Inquilino.query.all()
    contrato = Contrato.query.all()
    imovel = Imovel.query.all()
    corretor = Corretor.query.all()

    if request.method == 'GET':
        return render_template('update_aluguel.html', aluguel=aluguel, corretor=corretor, imovel=imovel, contrato=contrato, inquilino=inquilino)

    if request.method == 'POST':
        aluguel.id_corretor = request.form["id_corretor"]
        aluguel.id_imovel = request.form["id_imovel"]
        aluguel.id_contrato = request.form["id_contrato"]
        aluguel.id_inquilino = request.form["id_inquilino"]
        aluguel.valor = request.form["valor"]
        aluguel.exige_calcao = request.form["exige_calcao"]
        aluguel.aceita_melhorias = request.form["aceita_melhorias"]

        db.session.add(aluguel)
        db.session.commit()

        flash('Aluguel atualizado com sucesso')
        return redirect(url_for('show_all_alugueis'))


# Rotas delete
@app.route('/inquilino_delete/<id>', methods=['GET', 'POST'])
def inquilino_delete(id):
    inquilino = Inquilino.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_inquilino.html', inquilino=inquilino)
    if request.method == 'POST':
        if inquilino:
            db.session.delete(inquilino)
            db.session.commit()
            flash('Inquilino excluído com sucesso')
            return redirect(url_for('show_all_inquilinos'))
        abort(404)


@app.route('/proprietario_delete/<id>', methods=['GET', 'POST'])
def proprietario_delete(id):
    proprietario = Proprietario.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_proprietario.html', proprietario=proprietario)
    if request.method == 'POST':
        if proprietario:
            db.session.delete(proprietario)
            db.session.commit()
            flash('Proprietario excluído com sucesso')
            return redirect(url_for('show_all_proprietarios'))
        abort(404)


@app.route('/corretor_delete/<id>', methods=['GET', 'POST'])
def corretor_delete(id):
    corretor = Corretor.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_corretor.html', corretor=corretor)
    if request.method == 'POST':
        if corretor:
            db.session.delete(corretor)
            db.session.commit()
            flash('Corretor excluído com sucesso')
            return redirect(url_for('show_all_corretores'))
        abort(404)


@app.route('/imovel_delete/<id>', methods=['GET', 'POST'])
def imovel_delete(id):
    imovel = Imovel.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_imovel.html', imovel=imovel)
    if request.method == 'POST':
        if imovel:
            db.session.delete(imovel)
            db.session.commit()
            flash('Imóvel excluído com sucesso')
            return redirect(url_for('show_all_imoveis'))
        abort(404)


@app.route('/contrato_delete/<id>', methods=['GET', 'POST', 'DELETE'])
def contrato_delete(id):
    contrato = Contrato.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_contrato.html', contrato=contrato)
    if request.method == 'POST':
        if contrato:
            db.session.delete(contrato)
            db.session.commit()
            flash('Imóvel excluído com sucesso')
            return redirect(url_for('show_all_contratos'))
        abort(404)


@app.route('/aluguel_delete/<id>', methods=['GET', 'POST'])
def aluguel_delete(id):
    aluguel = Aluguel.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('delete_aluguel.html', aluguel=aluguel)
    if request.method == 'POST':
        if aluguel:
            db.session.delete(aluguel)
            db.session.commit()
            flash('Aluguel excluído com sucesso')
            return redirect(url_for('show_all_alugueis'))
        abort(404)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
