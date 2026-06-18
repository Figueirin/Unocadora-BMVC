import os
import bottle
from bottle import Bottle, run, request, redirect, template, response, static_file
from controllers.aplicacao import Aplicacao

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bottle.TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'views'))

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

    return template('login.html', erro=erro)

@app.route('/logout')
def logout():
    response.delete_cookie("usuario", path='/')
    return redirect('/portal')

@app.route('/cadastro', method=['GET', 'POST'])
def cadastro():
    if obter_usuario_logado():
        return redirect('/')

    erro = None

    if request.method == 'POST':
        nome = request.forms.get('nome')
        cpf = request.forms.get('cpf')
        telefone = request.forms.get('telefone')
        username = request.forms.get('username')
        password = request.forms.get('password')

        try:
            ctl.cadastrar_cliente(nome, cpf, telefone, username, password)
            response.set_cookie("usuario", username, secret=SECRET_KEY, path='/')
            return redirect('/')
        except ValueError as e:
            erro = str(e)

    return template('cadastro.html', erro=erro)

@app.route('/')
def home():
    username = obter_usuario_logado()
    if not username:
        return template('cardapio.html', veiculos=ctl.veiculos, usuario=None)

    cliente = ctl.obter_cliente_por_user(username)
    if cliente:
        return template('cardapio.html', veiculos=ctl.veiculos, usuario=username)
    else:
        stats = {
            "total_clientes": len(ctl.clientes),
            "total_veiculos": len(ctl.veiculos),
            "total_locacoes": len(ctl.locacoes)
        }
        return template('home.html', stats=stats, usuario=username)

@app.route('/clientes', method=['GET', 'POST'])
def clientes():
    username = obter_usuario_logado()
    if not username:
        return redirect('/portal')

    if ctl.obter_cliente_por_user(username):
        return redirect('/')

    erro = None
    if request.method == 'POST':    
        nome = request.forms.get('nome')
        cpf = request.forms.get('cpf')
        telefone = request.forms.get('telefone')
        user_cli = request.forms.get('username')
        pass_cli = request.forms.get('password')
        try:
            ctl.cadastrar_cliente(nome, cpf, telefone, user_cli, pass_cli)
            return redirect('/clientes')
        except ValueError as e:
            erro = str(e)

    return template('clientes.html', clientes=ctl.clientes, erro=erro, usuario=username)

@app.route('/veiculos', method=['GET', 'POST'])
def veiculos():
    username = obter_usuario_logado()
    if not username:
        return redirect('/portal')

    if ctl.obter_cliente_por_user(username):
        return redirect('/')

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

    return template('veiculos.html', veiculos=ctl.veiculos, erro=erro, usuario=username)

@app.route('/locacao', method=['GET', 'POST'])
def locacao():
    username = obter_usuario_logado()
    if not username:
        return redirect('/portal')

    cliente = ctl.obter_cliente_por_user(username)
    erro = None

    if request.method == 'POST':
        if cliente:
            cliente_cpf = cliente.cpf
        else:
            cliente_cpf = request.forms.get('cliente_cpf')

        veiculo_placa = request.forms.get('veiculo_placa')
        data_inicio = request.forms.get('data_inicio')
        data_final = request.forms.get('data_final')

        try:
            ctl.cadastrar_locacao(cliente_cpf, veiculo_placa, data_inicio, data_final)
            return redirect('/historico')
        except ValueError as e:
            erro = str(e)

    placa_pre_selecionada = request.query.get('placa', '')

    return template('locacao.html', 
                    clientes=ctl.clientes, 
                    veiculos=ctl.veiculos, 
                    erro=erro, 
                    usuario=username,
                    is_cliente=(cliente is not None),
                    placa_selecionada=placa_pre_selecionada)

@app.route('/historico')
def historico():

    username = obter_usuario_logado()
    if not username:
        return redirect('/portal')

    cliente = ctl.obter_cliente_por_user(username)

    if cliente:
        locacoes_filtradas = [l for l in ctl.locacoes if l.cliente.cpf == cliente.cpf]
        return template('historico.html', locacoes=locacoes_filtradas, usuario=username, is_cliente=True)
    else:
        return template('historico.html', locacoes=ctl.locacoes, usuario=username, is_cliente=False)
    
    

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)