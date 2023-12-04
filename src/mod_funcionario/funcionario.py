from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from mod_login.login import validaSessao
from flask import send_file
from mod_funcionario.GeraPdfFunc import PDF
import requests
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO
from funcoes import Funcoes
bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaFuncionario():
    try:
      response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API)
      result = response.json()
      if (response.status_code != 200):
          raise Exception(result[0])

      return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
      return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/form-funcionario/', methods=['POST'])
@validaSessao
def formFuncionario():
    return render_template('formFuncionario.html')

@bp_funcionario.route('/insert', methods=['POST'])
@validaSessao
def insert():
    try:

      id_funcionario = request.form['id']
      nome = request.form['nome']
      matricula = request.form['matricula']
      cpf = request.form['cpf']
      telefone = request.form['telefone']
      grupo = request.form['grupo']
      senha = Funcoes.cifraSenha(request.form['senha'])

      payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}

      response = requests.post(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, json=payload)
      result = response.json()
      print(result) 
      print(response.status_code) 

      if (response.status_code != 200 or result[1] != 200):
        raise Exception(result[0])

      return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    except Exception as e:
      return render_template('formListaFuncionario.html', msgErro=e.args[0])


@bp_funcionario.route('/form-edit-funcionario', methods=['POST'])
@validaSessao
def formEditFuncionario():
    try:
      id_funcionario = request.form['id']
      response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API)
      result = response.json()

      if (response.status_code != 200):
        raise Exception(result[0])

      return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
      return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/edit', methods=['POST'])
@validaSessao
def edit():
  try:
    id_funcionario = request.form['id']
    nome = request.form['nome']
    matricula = request.form['matricula']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    grupo = request.form['grupo']
    senha = Funcoes.cifraSenha(request.form['senha'])

    payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}

    response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API, json=payload)
    result = response.json()

    if (response.status_code != 200 or result[1] != 200):
      raise Exception(result[0])

    return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))

  except Exception as e:
    return render_template('formListaFuncionario.html', msgErro=e.args[0])



@bp_funcionario.route('/delete', methods=['POST'])
@validaSessao
def delete():
  try:
    id_funcionario = request.form['id_funcionario']
    response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API)
    result = response.json()

    if (response.status_code != 200 or result[1] != 200):
      raise Exception(result[0])

    return jsonify(erro=False, msg=result[0])

  except Exception as e:
    return jsonify(erro=True, msg=e.args[0])


@bp_funcionario.route('/pdfTodos', methods=['GET', 'POST'])
@validaSessao
def pdfTodos():
  geraPdf = PDF()
  geraPdf.listaTodos()
  return send_file('pdfFuncionarios.pdf')