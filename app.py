# app.py

from flask import Flask, render_template, redirect, url_for, jsonify
import oci
import time
from config import instance_id

app = Flask(__name__)

# Configuração da OCI
config = oci.config.from_file('/app/config')
compute_client = oci.core.ComputeClient(config)

# Substitua pelo ID da sua instância
INSTANCE_ID = instance_id

def get_instance_status(instance_id):
    instance = compute_client.get_instance(instance_id).data
    return instance.lifecycle_state

def start_instance(instance_id):
    compute_client.instance_action(instance_id, "START")
    # Não bloquear a aplicação esperando o estado mudar

def stop_instance(instance_id):
    compute_client.instance_action(instance_id, "SOFTSTOP")
    # Não bloquear a aplicação esperando o estado mudar

@app.route('/')
def index():
    status = get_instance_status(INSTANCE_ID)
    return render_template('index.html', status=status)

@app.route('/start')
def start():
    start_instance(INSTANCE_ID)
    return redirect(url_for('wait', action='Iniciando'))

@app.route('/stop')
def stop():
    stop_instance(INSTANCE_ID)
    return redirect(url_for('wait', action='Desligando'))

@app.route('/wait/<action>')
def wait(action):
    return render_template('wait.html', action=action)

@app.route('/status')
def get_status():
    status = get_instance_status(INSTANCE_ID)
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
