import eventlet
eventlet.monkey_patch() 
from celery.result import AsyncResult
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from googletrans import LANGUAGES
import os
from tasks import convert_file_task, translation_progress

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def get_language_code(language_name, LANGUAGES):
    for code, name in LANGUAGES.items():
        if name.lower() == language_name.lower():
            return code
    return "Language not found"


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return jsonify({'filename': filename}), 200

@app.route('/convert', methods=['POST'])
def convert_file():
    data = request.json
    filename = data.get('filename')
    mode = data.get('mode', 'book')
    src_lang = data.get('src_lang', None)
    tgt_lang = get_language_code(data.get('tgt_lang', None), LANGUAGES)
    chapter_num = data.get('chapter_num', '')
    
       # Get and normalize paths
    upload_path = app.config['UPLOAD_FOLDER']
    result_path = app.config['RESULT_FOLDER']
    
    # Extract file info
    if not filename:
        return jsonify({'error': 'Missing filename'}), 400
    
    input_filepath = os.path.join(upload_path, filename)
    
    if chapter_num and str(chapter_num).isdigit():
        chapter_num = int(chapter_num)

    # Build output filename
    base_name, ext = os.path.splitext(filename)
    output_filename = f"{mode}_{chapter_num}_{base_name}_translated.docx"
    output_filepath = os.path.join(result_path, output_filename)
    if not filename:
        return jsonify({'error': 'Missing filename'}), 400

    print(input_filepath)
    print(output_filepath)
    task = translation_progress.apply_async(args=[input_filepath, mode, src_lang, tgt_lang, output_filepath, chapter_num])
    return jsonify({'task_id': task.id}), 202

@app.route('/progress/<task_id>', methods=['GET'])
def task_progress(task_id):
   
    print('hello')
    task = AsyncResult(task_id)
    print('still alive')
    print(task.info)
    response = {
        'state': task.state,
        'info': task.info if task.info else ''
    }
    return jsonify(response)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
