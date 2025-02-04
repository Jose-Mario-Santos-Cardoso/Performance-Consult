from flask import Flask, request, send_file
import os
import shutil
import psutil
import subprocess
app = Flask(__name__)
#Definitn d'basePath
base_path = os.path.dirname(os.path.abspath(__file__))
streamlit_processes = []  #List t/armazen proces d'Streamlit
@app.route('/')
def index():
    return send_file(os.path.join(base_path, 'front-end', 'index.html'))
@app.route('/style.css')
def style():
    return send_file(os.path.join(base_path, 'front-end', 'style.css'))
@app.route('/script.js')
def script():
    return send_file(os.path.join(base_path, 'front-end', 'script.js'))
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(base_path, 'files', 'file.xlsx')
        file.save(file_path)
        return '', 204  #NoContent
    return 'Erro ao carregar o arquivo', 400
@app.route('/analyze')
def analyze():
    global streamlit_processes
    analysis_path = os.path.join(base_path, 'back-end', 'Analysis.py')
    process = subprocess.Popen(['streamlit', 'run', analysis_path, '--server.port', '8505'])
    streamlit_processes.append(process)
    return '', 204
@app.route('/shutdown', methods=['POST'])
def shutdown():
    clear_files()
    shutdown_streamlit()
    shutdown_server()
def clear_files():
    dir_path = os.path.join(base_path, 'files')
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Falha ao deletar {file_path}. Razão: {e}')
def shutdown_streamlit():
    global streamlit_processes
    for process in streamlit_processes:
        process.terminate()
        process.wait()
    streamlit_processes = []
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    os._exit(0)
if __name__ == '__main__':
    files_path = os.path.join(base_path, 'files')
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    app.run(port=5010)