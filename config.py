import os

class Config(object):
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or r'/Users/galant/Documents/Github/book_dictionary/upload_folder/'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DOWNLOAD_FOLDER = 'downloads'