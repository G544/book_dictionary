from docx.enum.section import WD_ORIENTATION
from backend.fb2_parser import Pars_and_tokenize
from docx import Document
from docx.oxml.ns import qn

class Book_Dictionary():
    def __init__(self, file, lang):
        ''' Modes = 'Chapter' - extract only define chapter,
        "chapters" - all but each new chapter conatins only new words,
        "chapters_ex" - all book but divided for chapters
        'Book' - dictionary for all book
        '''
        self.lang = lang
        self.filename = file
        self.book = Pars_and_tokenize(self.filename)
        self.document = Document()
        section = self.document.sections[0]
        sectPr = section._sectPr
        cols = sectPr.xpath('./w:cols')[0]
        cols.set(qn('w:num'), '4')
        cols.set(qn('w:space'), '20')  # Set space between columns to 10 points ->0.01"
        new_width, new_height = section.page_height, section.page_width
        section.orientation = WD_ORIENTATION.LANDSCAPE
        section.page_width = new_width
        section.page_height = new_height

    def convert(self,end_file, mode="chapter", chapter=1):
        self.end_file = end_file
        if mode == "chapter" and chapter:
            self.chapter = chapter
        if mode == 'chapter':
            self.chapter_mode()
        elif mode == 'chapters':
            self.chapters_mode()
        elif mode == 'chapters_ex':
            self.chapters_mode_ex()
        elif mode == 'book':
            self.book_mode()
        else:
            print('Wrong value for mode')

    def chapter_mode(self):
        self._add_text_to_file(self.book.translator(self.chapter, self.lang))
        self._write_to_file()

    def chapters_mode_ex(self):
        for i in range(self.book.num_chapters):
            self.document.add_paragraph(str(i) + '\n')
            self._add_text_to_file(self.book.translator(i, self.lang))
        self._write_to_file()

    def chapters_mode(self):
        full_dict = []
        for i in range(self.book.num_chapters):
            full_chapter = self.book.translator(i, self.lang)
            new_chapter = full_chapter
            list(map(new_chapter.__delitem__, filter(new_chapter.__contains__, full_dict)))
            head_letters = set([s[0].title() for s in list(new_chapter.keys())])
            for letter in head_letters:
                new_chapter[letter] = '  '
            new_chapter = dict(sorted(new_chapter.items(), key=lambda x: x[0].lower()))
            full_dict = list(set(full_dict + list(full_chapter.keys())))
            self.document.add_paragraph(str(i) + '\n')
            self._add_text_to_file(new_chapter)
        self._write_to_file()

    def book_mode(self):
        full_dict = {}
        for i in range(self.book.num_chapters):
            full_chapter = self.book.translator(i, self.lang)
            full_dict = {**full_dict, **full_chapter}
        full_dict = dict(sorted(full_dict.items(), key=lambda x: x[0].lower()))
        self._add_text_to_file(full_dict)
        self._write_to_file()

    def _add_text_to_file(self, dictionary):
        text = '\n'.join(list(' : '.join(pair) for pair in (dictionary.items())))
        paragraph = self.document.add_paragraph(text)
        paragraph.paragraph_format.space_after = 0

    def _write_to_file(self):
        self.document.save(self.end_file)
