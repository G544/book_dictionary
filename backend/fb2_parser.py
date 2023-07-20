from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from chardet.universaldetector import UniversalDetector
import chardet
import re
import nltk
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
nltk.download('punkt')

class Pars_and_tokenize():

    def __init__(self, file):
        self.file = file
        self.num_chapters, self.content_chapters = self.chapter_extractor(self.file)

    # This function extracts number of define chapter and returns text content and number of all chapters, for russian books only
    def chapter_extractor(self, file):
        rawdata = open(self.file, 'rb').read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        file_encoding = str(charenc)
        chapter_count = 0
        stop_words = ['комментарии', 'примечания', 'конец ознакомительного фрагмента']
        with open(file, 'r', encoding=file_encoding) as file:
            f = file.read()
            f = f.replace('\n', '')
            stroke = f
            reg_genre = '<title>(.+?)</title>'
            chapter = '<section>(.+?)</section>'
            last_name = re.findall(reg_genre, stroke)
            chapts = re.findall(chapter, stroke)
            new_chapts = []
            for chapter in chapts:
                flag = False
                for item in last_name:
                    if item in chapter:
                        flag = True
                        break
                if flag and len(chapter ) >100:
                    chapter_count += 1
                    new_chapts.append(chapter)
                elif len(new_chapts) >1:
                    new_chapts[-1] = new_chapts[-1] + chapter
            flag_end = False
            for word in stop_words:
                if word in new_chapts[-1].lower():
                    new_chapts.pop(-1)
                    chapter_count -= 1

            return chapter_count, new_chapts

    def content(self, num_chapt):
        return self.content_chapters[num_chapt-1]

    def clean_content(self, num_chapt):
        text = self.content_chapters[num_chapt-1]
        tags = ['<title>', '</title>', '<p>', '</p>', '<strong>', '</strong>', '\xa0', '<emphasis>', '</emphasis>',
                '<section>', '</section>', '<epigraph>', '</epigraph>', '<cite>', '</cite>', '<table>', '</table>'
                                                                                                        '<empty-line>',
                '/<empty-line>', '<a>', '</a>', '<binary>', '</binary>', ]

        for tag in tags:
            text = text.replace(tag, ' ')

        text = re.sub('<image(.+?)/>', '', text, flags=re.DOTALL)
        return text

    def tokenize(self, num_chapt, language = 'russian'):
        return self._tokenize(self.clean_content(num_chapt), language = 'russian')

    def _tokenize(self, text, language = 'russian'):
        punctuation_marks_nums = ['``','"',"«","»","'",'.','…',',','!','?','-',';',':','(',')','–','—','/','<','>','0','1','2','3','4','5','6','7','8','9']
        flag = False
        count_words = {}
        for word in word_tokenize(text.lower(), language= language):
            for mark in punctuation_marks_nums:
                if mark in word:
                    flag = True
                    break
            if flag:
                flag = False
                continue
            if word in count_words:
                count_words[word]+= 1
            else:
                count_words[word] = 1

        return count_words


    def translator(self, num_chapt, des_language, init_language='auto', extend = False):
        translator = GoogleTranslator(source=init_language, target=des_language)
        tokens = list(self.tokenize(num_chapt).keys())
        length = len(tokens)
        data = []
        x = 0
        while length >= 250:
            data.append('\n '.join(tokens[x:x + 250]))
            x += 250
            length -= 250
        data.append('\n '.join(tokens[x:]))
        translated_content = []
        for word in data:
            translated_content.append(translator.translate(word))
        translated_content = '\n'. join(translated_content).split('\n')
        init_content = '\n'.join(data).split('\n')
        dictionary = {a:b for a,b in zip(init_content, translated_content)}
        inv_dict = {}
        for w, t in dictionary.items():
            t = t.strip().lower()
            if t!='' and len(t)>1:
                if t in inv_dict and w[1] == inv_dict[t][0][0]:
                    inv_dict[t].append(w.lstrip())
                else:
                    inv_dict[t] = [w.lstrip()]
        dictionary = {}
        for k, v in inv_dict.items():
            dictionary[' ,'.join(v)] = k
        head_letters = set([s[0].title() for s in list(dictionary.keys())])
        for letter in head_letters:
            dictionary[letter] = '  '
        dictionary = dict(sorted(dictionary.items(), key=lambda x: x[0].lower()))
        if extend:
            return dictionary, init_content, translated_content
        else:
            return dictionary


    def write_to_file(self, file_name, dictionary):
        document = Document()
        section = document.sections[0]
        sectPr = section._sectPr
        cols = sectPr.xpath('./w:cols')[0]
        cols.set(qn('w:num'),'2')
        cols.set(qn('w:space'), '20')  # Set space between columns to 10 points ->0.01"
        text = '\n'.join(list(' : '.join(pair) for pair in (dictionary.items())))
        paragraph = document.add_paragraph(text)
        paragraph.paragraph_format.space_after = 0
        document.save(file_name)

        #text = '\n'.join(list(' : '.join(pair) for pair in (dictionary.items())))
        #with open(file_name, 'w') as f:
        #    f.write(text)

