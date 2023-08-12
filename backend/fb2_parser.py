from docx import Document
from docx.oxml.ns import qn
import chardet
import re
import nltk
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
from collections import Counter
nltk.download('punkt')

class Pars_and_tokenize():

    STOP_WORDS = ['комментарии', 'примечания', 'конец ознакомительного фрагмента']
    TITLE_REGEX = '<title>(.+?)</title>'  # should be a constant
    SECTION_REGEX = '<section>(.+?)</section>'
    TAGS = ['<title>', '</title>', '<p>', '</p>', '<strong>', '</strong>',
            '\xa0', '<emphasis>', '</emphasis>', '<section>', '</section>',
            '<epigraph>', '</epigraph>', '<cite>', '</cite>', '<table>', '</table>'
            '<empty-line>', '</empty-line>', '<a>', '</a>', '<binary>', '</binary>']
    PUNCT_MARKS = ['``', '"', "«", "»", "'", '.', '…', ',', '!', '?', '-', ';', ':', '(', ')',
                   '–', '—', '/', '<', '>', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    BATCH_SIZE_TRANSLATE = 250

    def __init__(self, file):
        self.file = file
        self.num_chapters, self.content_chapters = self.chapter_extractor(self.file)

    # This function extracts number of define chapter and returns text content and number of all chapters, for russian books only
    def chapter_extractor(self, file):
        # defining the file encoding for book
        with open(self.file, 'rb') as encode_file:
            rawdata_for_encoding = encode_file.read()
            file_encoding = chardet.detect(rawdata_for_encoding)
            file_encoding = str(file_encoding['encoding'])
        chapter_count = 0
        with open(file, 'r', encoding=file_encoding) as file:
            f = file.read()
            f = f.replace('\n', '')
            sections = re.findall(self.SECTION_REGEX, f)
            chapters = []
            # grouping by chapters
            for section in sections:
                flag_title = bool(re.findall(self.TITLE_REGEX, section))
                if flag_title and len(section) > 100:  # 100 should be a constant
                    chapter_count += 1
                    chapters.append(section)
                # For chapters which contain more than one section construct inside
                elif len(chapters) > 1:
                    chapters[-1] = chapters[-1] + section
            # remove complimentary chapters
            for word in self.STOP_WORDS:
                if word in chapters[-1].lower():
                    chapters.pop(-1)
                    chapter_count -= 1
            return chapter_count, chapters
    # return content for each chapter with all special characters
    def content(self, num_chapt):
        return self.content_chapters[num_chapt-1]

    # return content for each chapter without special characters
    def clean_content(self, num_chapt):
        text = self.content_chapters[num_chapt-1]
        for tag in self.TAGS:
            text = text.replace(tag, ' ')
        text = re.sub('<image(.+?)/>', '', text, flags=re.DOTALL)
        return text

# dividing text without tags into tokens and removing words with digits or punctuatin marks
    def tokenize(self, num_chapt, language = 'russian'):
        # it is better to redo by using regex something like \w+
        tokenized_data = list(filter(lambda x: not set(x).intersection(self.PUNCT_MARKS),
                                     word_tokenize(self.clean_content(num_chapt).lower(), language= language)))
        count_words = dict(Counter(tokenized_data))
        return count_words


    def translator(self, num_chapt, des_language, init_language='auto', extend = False):
        translator = GoogleTranslator(source=init_language, target=des_language)
        tokens = list(self.tokenize(num_chapt).keys())
        number_of_tokens = len(tokens)
        data = []
        batch_point = 0
        translated_content = []
        while number_of_tokens >= self.BATCH_SIZE_TRANSLATE:  #
            data.append('\n '.join(tokens[batch_point : batch_point + self.BATCH_SIZE_TRANSLATE]))
            translated_content.append(translator.translate('\n '.join(tokens[batch_point : batch_point + self.BATCH_SIZE_TRANSLATE])))
            batch_point += self.BATCH_SIZE_TRANSLATE
            number_of_tokens -= self.BATCH_SIZE_TRANSLATE
        # append the remains batch with size less than BATCH_SIZE
        data.append('\n '.join(tokens[batch_point:]))
        translated_content.append(translator.translate('\n '.join(tokens[batch_point:])))
        translated_content = '\n'. join(translated_content).split('\n')
        init_content = '\n'.join(data).split('\n')
        # creating dictionary
        dictionary = {a:b for a,b in zip(init_content, translated_content)}
        # invert dictionary and if values are equal keys will be joined into one string for example
        # d = {'a':'4', 'b':4}  into d = {'a, b':4}
        inv_dict = {}
        for w, t in dictionary.items():
            t = t.strip().lower()
            if t!='' and len(t)>1:
                if t in inv_dict and w[1] == inv_dict[t][0][0]:
                    inv_dict[t].append(w.lstrip())
                else:
                    inv_dict[t] = [w.lstrip()]
        for k, v in inv_dict.items():
            dictionary[' ,'.join(v)] = k
        # adding divide into first letters
        head_letters = set([s[0].title() for s in list(dictionary.keys())])
        for letter in head_letters:
            dictionary[letter] = '  '
        dictionary = dict(sorted(dictionary.items(), key=lambda x: x[0].lower()))
        if extend:
            return dictionary, init_content, translated_content
        else:
            return dictionary
