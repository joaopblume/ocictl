import oci
from flask import Flask, render_template, redirect, url_for
from config import instance_id

# Replace with the path to your config file
config = oci.config.from_file('C:/Users/joaop/ocictl/config')  
compute_client = oci.core.ComputeClient(config)

# Verify the instance status
def get_instance_status(instance_id):
    instance = compute_client.get_instance(instance_id).data
    return instance.lifecycle_state


# Turn on the vm
def start_instance(instance_id):
    compute_client.instance_action(instance_id, "START")


# Turn off the vm
def stop_instance(instance_id):
    compute_client.instance_action(instance_id, "SOFTSTOP")



# Start flask app
app = Flask(__name__)

# Replace with your instance OCID
INSTANCE_ID = instance_id

@app.route('/')
def index():
    status = get_instance_status(INSTANCE_ID)
    return render_template('index.html', status=status)

@app.route('/start')
def start():
    start_instance(INSTANCE_ID)
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    stop_instance(INSTANCE_ID)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)