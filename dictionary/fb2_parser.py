
from chardet.universaldetector import UniversalDetector
import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')


class Pars_and_tokenize():

    def __init__(self, file):
        self.file = file
        self.num_chapters, self.content_chapters = self.chapter_extractor(self.file)

    # This function extracts number of define chapter and returns text content and number of all chapters, for russian books only
    def chapter_extractor(self, file):
        detector = UniversalDetector()
        with open(file, 'rb') as file_encoding:
            for line in file_encoding:
                detector.feed(line)
                if detector.done:
                    break
        file_encoding = str(detector.result['encoding'])
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

    def tokenize(self, num_chapt):
        return self._tokenize(self.content_chapters[num_chapt-1])

    def _tokenize(self, text, language = 'russian'):
        count_words = {}
        for word in word_tokenize(text.lower(), language= language):
            if word in count_words:
                count_words[word]+= 1
            else:
                count_words[word] = 1

        return count_words