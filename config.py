import os

class Config(object):
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or r'C:\Users\79689\Documents\GitHub\book_dictionary\upload_folder'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'