import eventlet
eventlet.monkey_patch() 
from app import celery, socketio, application
from backend.convert import TranslationManager
from flask_socketio import SocketIO

@celery.task(bind=True)
def translation_progress(self, book,mode, src_lang, tgt_lang,filename, chapter_num):
     socketio = SocketIO(message_queue='redis://')
     translation_manager = TranslationManager(book,mode, src_lang, tgt_lang, chapter_num)
     dictionary = dict()
     translator = translation_manager.translate_book()
     amount_batches = len(translator.batches)-1
     for n_batch, translated_batch in translator.translation_batches():
         print(n_batch/amount_batches)
         dictionary.update(translated_batch)
         socketio.emit('progress', {'progress': round(n_batch/amount_batches*100,2)})
     translation_manager.write_to_file(dictionary, filename)