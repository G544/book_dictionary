import xml.etree.ElementTree as ET
import os
from bs4 import BeautifulSoup
import re
class Pars_and_tokenize():
    def __init__(self, filename, external_annotations=True):
        self.root = ET.parse(filename).getroot()
        self.cleanup()
        self.external_annotations = external_annotations  # doesn't implement at the moment
        self.main, *rest= self.root.findall('body')
        self.sections = {1:[]}
        self.chapters_name = {1 : []}
        self.chapter_cnt = 1
        self.go_into_branch(self.main)
        self.section_clean, self.chapters_name_clean = self.clean_chapters()
    
    def cleanup(self):
        for element in self.root.iter():
                element.tag = element.tag.partition('}')[-1]
    
    def _clean_after_text(self,text):
        # Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces, newlines, etc. with a single space
        text = re.sub(r'\xa0', ' ', text)  # Replace non-breaking spaces
        text = re.sub(r'\n', ' ', text)  # Remove newline characters
        text = re.sub(r'\t', ' ', text)  # Remove tab characters
        
        # Remove any remaining HTML entities
        text = re.sub(r'&[a-z]+;', '', text)
        
        return text.strip()
   
    def clean_chapters(self):
        sections_clean = {}
        for key, value in self.sections.items():
            sections_clean[key] = []
            for part in value:
                sections_clean[key].append(self._clean_after_text(part))
        chapters_name_clean = {}
        for key, value in self.chapters_name.items():
            chapters_name_clean[key] =self._clean_after_text(value)
        return sections_clean, chapters_name_clean

    
    def _innertext(self,tag):
        return (tag.text or '') + ''.join(self._innertext(e) for e in tag) + (tag.tail or '')
    

    def go_into_branch(self,branch):
        if not (branch.find('title') is None):
                if len(self.chapters_name[self.chapter_cnt]) == 0 or self.chapters_name[self.chapter_cnt][0] == '' or len(self.sections[self.chapter_cnt]) == 0:
                    pass
                else:
                    self.chapter_cnt += 1
                self.chapters_name[self.chapter_cnt] = self._innertext(branch.find('title'))
                self.sections[self.chapter_cnt] = []
                
        if (branch.find('section') is None):
                self.sections[self.chapter_cnt].append(self._innertext(branch))
                return 
        else:
            for part in branch.findall('section'):
                self.go_into_branch(part)
    