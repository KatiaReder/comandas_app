from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps

import requests
from settings import ENDPOINT_LOGIN, HEADERS_API
from funcoes import Funcoes
bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')
@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")

@bp_login.route('/login', methods=['POST'])
def validaLogin():
  try:

    cpf = request.form['usuario']
    grupo = request.form['grupo']
    senha = Funcoes.cifraSenha(request.form['senha'])
    
    session.clear();

    payload = {'cpf': cpf, 'senha': senha, 'grupo': grupo}  
 

    response = requests.post(ENDPOINT_LOGIN, headers=HEADERS_API, json=payload)
    result = response.json()

   # if (cpf == "abc" and senha == Funcoes.cifraSenha('Bolinhas')) | (cpf == "xyz" and senha == Funcoes.cifraSenha('Quadrados')):

    if (result.cpf == cpf and result.senha == senha):
      session['login'] = cpf
      session['grupo'] = grupo
  
      return redirect(url_for('index.formIndex'))
    else:
      raise Exception("Falha de Login! Verifique seus dados e tente novamente!")

  except Exception as e:

    return redirect(url_for('login.login', msgErro=e.args[0]))
  

@bp_login.route("/logoff", methods=['GET'])
def logoff():

  session.pop('login', None)

  session.clear()

  return redirect(url_for('login.login'))



def validaSessao(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'login' not in session:
        return redirect(url_for('login.login', msgErro='Usuário não logado!'))
    else:
        return f(*args, **kwargs)

  return decorated_function