from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from mod_login.login import validaSessao
from flask import send_file
from mod_cliente.GeraPdfCliente import PDF
import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE
from funcoes import Funcoes
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

@bp_cliente.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaCliente():
  try:
    response = requests.get(ENDPOINT_CLIENTE, headers=HEADERS_API)
    result = response.json()
    if (response.status_code != 200):
      raise Exception(result[0])

    return render_template('formListaCliente.html', result=result[0])
  except Exception as e:
    return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/', methods=['POST'])
@validaSessao
def formCliente():
  return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])
@validaSessao
def insert(): 
  try:
    id_cliente = request.form['id']
    nome = request.form['nome']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    dia_fiado = request.form['dia_fiado']
    compra_fiado = request.form['compra_fiado']
    senha = Funcoes.cifraSenha(request.form['senha'])

    payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'dia_fiado': dia_fiado, 'compra_fiado': compra_fiado, 'senha': senha}

    response = requests.post(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload)
    result = response.json()
    print(result)
    print(response.status_code)

    if (response.status_code != 200 or result[1] != 200):
      raise Exception(result[0])

    return redirect(url_for('cliente.formListaCliente', msg=result[0]))
  except Exception as e:
    return render_template('formListaCliente.html', msgErro=e.args[0])


@bp_cliente.route('/form-edit-cliente', methods=['POST'])
@validaSessao
def formEditCliente():
  try:
    id_cliente = request.form['id']
    response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
    result = response.json()

    if (response.status_code != 200):
      raise Exception(result[0])

    return render_template('formCliente.html', result=result[0])
  except Exception as e:
    return render_template('formListaCliente.html', msgErro=e.args[0])


@bp_cliente.route('/edit', methods=['POST'])
@validaSessao
def edit():
  try:
    id_cliente = request.form['id']
    nome = request.form['nome']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    dia_fiado = request.form['dia_fiado']
    compra_fiado = request.form['compra_fiado']
    senha = Funcoes.cifraSenha(request.form['senha'])

    payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'dia_fiado': dia_fiado, 'compra_fiado': compra_fiado, 'senha': senha}

    response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, json=payload)
    result = response.json()

    if (response.status_code != 200 or result[1] != 200):
      raise Exception(result[0])

    return redirect(url_for('cliente.formListaCliente', msg=result[0]))

  except Exception as e:
    return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/delete', methods=['POST'])
@validaSessao
def delete():
  try:
    id_cliente = request.form['id_cliente']
    response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
    result = response.json()

    if (response.status_code != 200 or result[1] != 200):
      raise Exception(result[0])

    return jsonify(erro=False, msg=result[0])
  except Exception as e:
    return jsonify(erro=True, msgErro=e.args[0])
  
@bp_cliente.route('/pdfTodos', methods=['GET', 'POST'])
@validaSessao
def pdfTodos():
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('pdfClientes.pdf')