
from backend.fb2_parser_new import Pars_and_tokenize
from backend.tokenizer import PrepareWordList
from backend.translator import Translate
from backend.writer import SaveToDoc


class TranslationManager():
    def __init__(self, book:str, mode:str, src_lang:str, tgt_lang:str,chapter_num:int = -1):
        self.book = book
        self.mode = mode
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.chapter_num = chapter_num
        
    @staticmethod
    def assemble_chapter(self, wordlist, translation_dict, writed_set = set()):
        chapter_translations = {}
        for word in wordlist:
            if len(word)>2 and (not word.isdigit()) and (word not in writed_set):
                chapter_translations[word] = translation_dict[word]
                writed_set.add(word)
        return chapter_translations, writed_set


    def translate_book(self): #-> Translate
        book_proceed = Pars_and_tokenize(self.book)
        self.pwl = PrepareWordList(book_proceed.section_clean, self.src_lang)
        trans = Translate(self.pwl.tokenize(self.mode, self.chapter_num), self.tgt_lang)
        return trans
   
    
    def write_to_file(self, dictionary:dict, filename:str):
        file = SaveToDoc(filename)
        if self.mode == 'chapter' or self.mode == 'book':
            file.add_text_to_file(dictionary)
            file.write_to_file()
        elif self.mode == 'chapters' or self.mode == 'chapters_ex':
            chapters_wordlist = self.pwl.tokenize('chapters')
            writed_set = set()
            for chapter_number, chapter in chapters_wordlist.items():
                if self.mode == "chapters_ex":
                    chapter_dictionary, writed_set = self.assemble_chapter(chapter, dictionary, set())
                elif self.mode == "chapters":
                    chapter_dictionary, writed_set = self.assemble_chapter(chapter, dictionary,writed_set)
                file.add_chapter(f'\nChapter {chapter_number}\n')
                file.add_text_to_file(chapter_dictionary)
        file.write_to_file()
    
