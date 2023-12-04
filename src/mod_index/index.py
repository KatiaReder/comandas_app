from flask import Blueprint, render_template
bp_index = Blueprint('index', __name__, template_folder='templates', url_prefix='/home')

@bp_index.route('/')
def formIndex():
  return render_template('formIndex.html'), 200