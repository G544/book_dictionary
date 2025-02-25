from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

class PrepareWordList():
    def __init__(self, chapters, language):
        self.chapters = chapters
        self.language = language
        
    def tokenize(self, mode, num=-1):
        if mode == 'chapter' and num > -1:
            return {num: self._tokenization('\n'.join(self.chapters[num]))}
        elif mode in ['chapters', 'chapters_ex','book']:
            tokenized_chapters = {}
            for chapter_index, chapter in self.chapters.items():
                tokenized_chapters[chapter_index] =self._tokenization('\n'.join(chapter))
            return tokenized_chapters
        else:
            print('Wrong value for mode')
    
    def _tokenization(self, text):
        tokenized_data = list(filter(lambda x: x.isalpha(),
                                     word_tokenize(text.lower(), language= self.language)))
        return tokenized_data
