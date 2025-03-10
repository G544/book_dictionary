from googletrans import Translator
import time

class Translate():
    KOEF = 0.011*2
    AMOUNT = 250
    def __init__(self,data, lang):
        self.data = data
        self.lang= lang
        self.all_words = self.preparation()
        self.translator = Translator()
        self.estimation()
        self.batches = [self.all_words[i:i + self.AMOUNT] for i in range(0, len(self.all_words), self.AMOUNT)]
        


        
    def estimation(self, precise = False):
        n = len(self.all_words)
        start = time.time()
        if precise:
            self.translator.translate('\n'.join(self.all_words[0:self.AMOUNT]), dest =self.lang).text
            self.KOEF = (time.time() - start)/60*2
            print(self.KOEF)
        print(f'Time of translation ~ {round(self.KOEF*(n//self.AMOUNT),1)} min')
   
        
    
    def translation(self):
        batches = [self.all_words[i:i + self.AMOUNT] for i in range(0, len(self.all_words), self.AMOUNT)]
        translated = {}
        for i, batch in enumerate(batches):
            translated_batch = self.translator.translate('\n'.join(batch), dest =self.lang).text
            if len(batch) == len(translated_batch.split('\n')):
                translated.update({s:t for s,t in zip(batch, translated_batch.split('\n'))})
                
        return translated
    
    def translation_batches(self):
        translated = {}
        for num_batch, batch in enumerate(self.batches):
            translated_batch = self.translator.translate('\n'.join(batch), dest =self.lang).text
            if len(batch) == len(translated_batch.split('\n')):
                translated = {s:t for s,t in zip(batch, translated_batch.split('\n'))}
            yield num_batch, translated
        # return translated
    
    def preparation(self):
        all_words = []
        for _, chapter in self.data.items():
            all_words += chapter
        return list(set(all_words))