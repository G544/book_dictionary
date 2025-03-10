import eventlet
eventlet.monkey_patch() 
from flask import render_template,request, session, send_from_directory,current_app, redirect, jsonify
from app import application
import os
from werkzeug.utils import secure_filename
from googletrans import LANGUAGES
from backend.convert import TranslationManager
import time

from app.tasks import translation_progress







def get_language_code(language_name, LANGUAGES):
    for code, name in LANGUAGES.items():
        if name.lower() == language_name.lower():
            return code
    return "Language not found"


# Ensure folders exist
os.makedirs(application.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(application.config['DOWNLOAD_FOLDER'], exist_ok=True)

def get_language_code(language_name, LANGUAGES):
    for code, name in LANGUAGES.items():
        if name.lower() == language_name.lower():
            return code
    return "Language not found"

    
@application.route('/')
@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            session['my_var'] = filename
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            session['uploaded'] = True
            return redirect('/settings')
    return render_template("upload.html")

@application.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('uploaded'):
        return redirect('/upload')

    languages = list(LANGUAGES.values())

    if request.method == 'POST':
        session['dest_language'] = request.form.get('dest_language')
        session['src_language'] = request.form.get('src_language')
        session['mode'] = request.form.get('mode')
        session['chapter_num'] = request.form.get('chapter', '')
        return redirect('/convert')

    return render_template("settings.html", languages=languages)


@application.route('/convert', methods=['GET', 'POST'])
def start_translation():
    

    # task = download_page.apply_async()
    # return jsonify({"task_id": task.id}) socketio = SocketIO(message_queue='redis://')
    path = application.config['UPLOAD_FOLDER']
    final_doc = 'convert_'+str(session.get('my_var', None)).replace('.fb2', '.docx')
    language = get_language_code(session.get('dest_language', None), LANGUAGES)
    mode = session.get('mode', 'book')
    download_path = os.path.join(current_app.root_path, application.config['DOWNLOAD_FOLDER'])
    #  if request.method == 'POST':
    book = path + str(session.get('my_var', None))
    chapter_num= session.get('chapter_num', '')
    if chapter_num.isdigit():
         chapter_num = int(chapter_num)
    src_lang = 'russian'
    tgt_lang = language
    final_doc = f'{mode}_' + str(chapter_num)  + '_' + final_doc
    filename = '//'.join([download_path,final_doc])
    task = translation_progress.apply_async(args=[
        book,mode, src_lang, tgt_lang,filename, chapter_num
     ])
    print(f'Task_id: {task.id}')
    if 'home' in request.form:
        return redirect('/upload')
    return render_template('progress.html')
# render_template('convert_and_download.html', filename=final_doc)

@application.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
     print(current_app.root_path)
     downloads = os.path.join(current_app.root_path, application.config['DOWNLOAD_FOLDER'])
     session['filename'] = filename
     return send_from_directory(downloads, filename, as_attachment=True)
