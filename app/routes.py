from flask import render_template,request, session
from app import app
import os
from werkzeug.utils import secure_filename
from backend.Pars_options import Book_Dictionary


@app.route('/')
@app.route('/upload')
def upload():
    return render_template("file_upload_form.html", title='Home')


@app.route('/next_step', methods=['POST'])
def select_page():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)
    session['my_var'] = filename
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("select_converting_type.html", name=f.filename)


@app.route('/convert_step', methods=['POST'])
def download_page():
    path = r'C:\Users\79689\Documents\GitHub\book_dictionary\upload_folder\\'
    final_doc = 'convert_'+str(session.get('my_var', None)).replace('.fb2', '.docx')
    if request.method == 'POST':
        if 'chapter' in request.form:
            value = "THING1"
            final_doc = 'chapter_'+ final_doc
            book = Book_Dictionary(path+str(session.get('my_var', None)), final_doc, mode='chapter', chapter=1)
            book.convert()
        elif 'chapters' in request.form:
            value = "THING2"
            final_doc = 'chapters_'+ final_doc
            book = Book_Dictionary(path+str(session.get('my_var', None)), final_doc, mode='chapters')
            book.convert()
        elif 'chapters_ex' in request.form:
            value = "THING3"
            final_doc = 'chapters_ex_'+ final_doc
            book = Book_Dictionary(path+str(session.get('my_var', None)), final_doc, mode='chapters_ex')
            book.convert()
        elif 'book' in request.form:
            value = "THING4"
            final_doc = 'book_'+ final_doc
            book = Book_Dictionary(path+str(session.get('my_var', None)), final_doc, mode='book')
            book.convert()
        else:
            pass # unknown
        return render_template('convert_and_download.html', value=value)