
from backend.fb2_parser_new import Pars_and_tokenize
from backend.tokenizer import PrepareWordList
from backend.translator import Translate
from backend.writer import SaveToDoc

def assemble_chapter(wordlist, translation_dict, writed_set = set()):
    chapter_translations = {}
    for word in wordlist:
        if len(word)>2 and (not word.isdigit()) and (word not in writed_set):
            chapter_translations[word] = translation_dict[word]
            writed_set.add(word)
    return chapter_translations, writed_set

def convert_book(book:str, mode:str, src_lang:str, tgt_lang:str, filename:str ,chapter_num:int = -1):
   
    book_proceed = Pars_and_tokenize(book)
    pwl = PrepareWordList(book_proceed.section_clean, src_lang)
    if mode == 'chapter':
        trans = Translate(pwl.tokenize('chapter', chapter_num), tgt_lang)
        dictionary = trans.translation()
        file = SaveToDoc(filename)
        file.add_text_to_file(dictionary)
        file.write_to_file()
    elif mode == 'chapters' or mode == 'chapters_ex':
        chapters_wordlist = pwl.tokenize('chapters')
        trans = Translate(chapters_wordlist, tgt_lang)
        file = SaveToDoc(filename)
        dictionary = trans.translation()
        writed_set = set()
        for chapter_number, chapter in chapters_wordlist.items():
            if mode == "chapters_ex":
                chapter_dictionary, writed_set = assemble_chapter(chapter, dictionary, set())
            elif mode == "chapters":
                chapter_dictionary, writed_set = assemble_chapter(chapter, dictionary,writed_set)
            file.add_chapter(f'\nChapter {chapter_number}\n')
            file.add_text_to_file(chapter_dictionary)
            print(len(writed_set))
            print(len(chapter_dictionary))
        file.write_to_file()
    elif mode == "book":
        trans = Translate(pwl.tokenize('book'), tgt_lang)
        dictionary = trans.translation()
        file = SaveToDoc(filename)
        file.add_text_to_file(dictionary)
        file.write_to_file()
            
        