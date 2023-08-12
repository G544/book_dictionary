from flask import render_template,request, session, send_from_directory,current_app
from app import application
import os
from werkzeug.utils import secure_filename
from backend.Pars_options import Book_Dictionary
from deep_translator import GoogleTranslator

@application.route('/')
@application.route('/upload')
def upload():
    return render_template("file_upload_form.html", title='Home')

@application.route('/language', methods=['POST','GET'])
def dropdown():
     if request.method == 'POST':
         f = request.files['file']
         if f:
             filename = secure_filename(f.filename)
     session['my_var'] = filename
     f.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
     gtranslator = GoogleTranslator()
     languages = gtranslator.get_supported_languages()
     return render_template("language_select.html", languages=languages, name=f.filename)



@application.route('/mode_step', methods=['POST'])
def mode_select():
     dropdownval = request.form.get('language')
     session['language'] = dropdownval
     return render_template('select_converting_type.html')

@application.route('/chapter', methods=['POST'])
def chapter_num_input():
     return render_template('number_of_chapter.html')

@application.route('/convert_step', methods=['POST'])
def download_page():
     path = r'C:\Users\79689\Documents\GitHub\book_dictionary\upload_folder\\'
     final_doc = 'convert_'+str(session.get('my_var', None)).replace('.fb2', '.docx')
     language = session.get('language', None)
     if request.method == 'POST':
         book = Book_Dictionary(path + str(session.get('my_var', None)), language)
         if 'chapter' in request.form:
             chapter_num = int(request.form.get('chapter'))
             final_doc = 'chapter_' + str(chapter_num)  + '_' + final_doc
             value = "THING1"
             book.convert(mode='chapter', chapter=chapter_num, end_file=final_doc)
         elif 'chapters' in request.form:
             final_doc = 'chapters_' + final_doc
             value = "THING2"
             book.convert( mode='chapters', end_file=final_doc)
         elif 'chapters_ex' in request.form:
             value = "THING3"
             final_doc = 'chapters_ex_' + final_doc
             book.convert( mode='chapters_ex', end_file=final_doc)
         elif 'book' in request.form:
             value = "THING4"
             final_doc = 'full_book_' + final_doc
             book.convert(mode='book', end_file=final_doc)
         else:
             pass # unknown
       #  return redirect('/upload')#s/' + final_doc)
         return render_template('convert_and_download.html', filename=final_doc)

@application.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
     downloads = os.path.join(current_app.root_path, application.config['DOWNLOAD_FOLDER'])
     return send_from_directory(downloads, filename, as_attachment=True)
