import eventlet
eventlet.monkey_patch() 
from celery import Celery
from flask_socketio import SocketIO
from backend.convert import TranslationManager


celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

celery_app.conf.update(
    broker='redis://localhost:6379/0',  # Message broker (e.g., Redis, RabbitMQ)
    result_backend='redis://localhost:6379/0',  # Result backend to store task results
    task_serializer='json',  # Serialize task data to JSON format
    result_serializer='json',  # Serialize results to JSON
    accept_content=['json'],  # Only accept JSON content
    timezone='UTC',  # Define the time zone for your tasks
)
socketio = SocketIO(message_queue='redis://localhost:6379/0')

@celery_app.task(bind=True)
def convert_file_task(self, input_path, output_path, src_lang):
    try:
        self.update_state(state='PROCESSING', meta={'step': 'initializing'})
        translator = TranslationManager(src_lang=src_lang)
        
        self.update_state(state='PROCESSING', meta={'step': 'translating'})
        translator.convert(input_path, output_path)  # Assuming this method exists
        
        return {'status': 'completed', 'output_file': output_path}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}


@celery_app.task(bind=True)
def translation_progress(self, book, mode, src_lang, tgt_lang, filename, chapter_num):
    try:
        self.update_state(state='PROCESSING', meta={'step': 'initializing'})
        
        socketio = SocketIO(message_queue='redis://')
        translation_manager = TranslationManager(book, mode, src_lang, tgt_lang, chapter_num)
        translator = translation_manager.translate_book()
        total_batches = len(translator.batches)

        dictionary = {}
        
        for n_batch, translated_batch in translator.translation_batches():
            progress = round((n_batch + 1) / total_batches * 100, 2)
            dictionary.update(translated_batch)
            socketio.emit('progress', {'progress': progress})
            self.update_state(state='PROCESSING', meta={'progress': progress})
        
        translation_manager.write_to_file(dictionary, filename)

        return {'status': 'completed', 'output_file': filename}
    
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        print(str(e))
        return {'status': 'failed', 'error': str(e)}
