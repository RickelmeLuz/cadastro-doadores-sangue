from flask import Blueprint, redirect, render_template, url_for

prototipo_bp = Blueprint(
    'prototipo',
    __name__,
    url_prefix='/prototipo')


@prototipo_bp.route('/')
def raiz():
    return redirect(url_for('prototipo.inicio'))


@prototipo_bp.route('/inicio')
def inicio():
    return render_template('publico/inicio.html')
