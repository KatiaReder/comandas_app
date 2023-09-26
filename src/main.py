from flask import Flask

from mod_funcionario.funcionario import bp_funcionario
from mod_index.index import bp_index
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
app = Flask(__name__)

app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_index)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)