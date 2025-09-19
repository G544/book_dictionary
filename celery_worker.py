from tasks import celery_app
import nltk
nltk.data.path.append('/opt/homebrew/anaconda3/envs/book_dictionary/nltk_data')
nltk.download('punkt')




if __name__ == '__main__':
    celery_app.worker_main()
