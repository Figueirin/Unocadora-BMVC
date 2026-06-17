import os
import bottle
from bottle import Bottle, run, request, redirect, template, response, static_file
from controllers.aplicacao import Aplicacao

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bottle.TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'views', 'html'))

app = Bottle()
ctl = Aplicacao()

SECRET_KEY = "unocadora_super_secret_key"

def obter_usuario_logado():
    return request.get_cookie("usuario", secret=SECRET_KEY)


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/portal', method=['GET', 'POST'])
def portal():
    if obter_usuario_logado():
        return redirect('/')

    erro = None

    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')

        if ctl.login(username, password):
            response.set_cookie("usuario", username, secret=SECRET_KEY, path='/')
            return redirect('/')
        else:
            erro = "Usuario ou senha incorretos"

    return template('login', erro=erro)

@app.route('/logout')
def logout():
    response.delete_cookie("usuario", path='/')
    return redirect('/portal')

@app.route('/')
def home():
    if not obter_usuario_logado():
        return redirect('/portal')

    stats = {
        "total_clientes": len(ctl.clientes),
        "total_veiculos": len(ctl.veiculos),
        "total_locacoes": len(ctl.locacoes)
    }
    return template('home', stats=stats, usuario=obter_usuario_logado())

@app.route('/clientes', method=['GET', 'POST'])
def clientes():
    if not obter_usuario_logado():
        return redirect('/portal')

    erro = None
    if request.method == 'POST':    
        nome = request.forms.get('nome')
        cpf = request.forms.get('cpf')
        telefone = request.forms.get('telefone')
        try:
            ctl.cadastrar_cliente(nome, cpf, telefone)
            return redirect('/clientes')
        except ValueError as e:
            erro = str(e)

    return template('clientes', clientes=ctl.clientes, erro=erro, usuario=obter_usuario_logado())

@app.route('/veiculos', method=['GET', 'POST'])
def veiculos():
    if not obter_usuario_logado():
        return redirect('/portal')

    erro = None

    if request.method == 'POST':
        placa = request.forms.get('placa')
        marca = request.forms.get('marca')
        modelo = request.forms.get('modelo')
        ano = request.forms.get('ano')
        tipo = request.forms.get('tipo')

        try:
            ctl.cadastrar_veiculo(placa, modelo, marca, int(ano), tipo)
            return redirect('/veiculos')
        except ValueError as e:
            erro = str(e)

    return template('veiculos', veiculos=ctl.veiculos, erro=erro, usuario=obter_usuario_logado())

@app.route('/locacao', method=['GET', 'POST'])
def locacao():
    if not obter_usuario_logado():
        return redirect('/portal')

    erro = None

    if request.method == 'POST':
        cliente_cpf = request.forms.get('cliente_cpf')
        veiculo_placa = request.forms.get('veiculo_placa')
        data_inicio = request.forms.get('data_inicio')
        data_final = request.forms.get('data_final')

        try:
            ctl.cadastrar_locacao(cliente_cpf, veiculo_placa, data_inicio, data_final)
            return redirect('/historico')
        except ValueError as e:
            erro = str(e)

    return template('locacao', clientes=ctl.clientes, veiculos=ctl.veiculos, erro=erro, usuario=obter_usuario_logado())

@app.route('/historico')
def historico():
    if not obter_usuario_logado():
        return redirect('/portal')
    
    return template('historico', locacoes=ctl.locacoes, usuario=obter_usuario_logado())

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)