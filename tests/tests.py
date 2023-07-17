from dictionary.fb2_parser import Pars_and_tokenize
import unittest


class TestParser(unittest.TestCase):
      def setUp(self):
          self.bulgakov = Pars_and_tokenize('C:/Users/79689/Documents/GitHub/book_dictionary/books/Bulgakov_Mihail__Master_i_Margarita__Readli.Net_256.fb2')
          self.monte_cristo = Pars_and_tokenize('C:/Users/79689/Documents/GitHub/book_dictionary/books/498373.fb2')
          self.little_prince = Pars_and_tokenize('C:/Users/79689/Documents/GitHub/book_dictionary/books/65.fb2')
          self.mur_chant = Pars_and_tokenize('C:/Users/79689/Documents/GitHub/book_dictionary/books/81695427.fb2')

class TestInit(TestParser):
      def test_bulgakov_num_chapters(self):
          self.assertEqual(self.bulgakov.num_chapters, 33)

      def test_bulgakov_last_chapter(self):
          self.assertEqual(self.bulgakov.content_chapters[33-1].split('</title>')[0], '<title><p>Эпилог</p>')

      def test_monte_cristo_number_of_chapters(self):
          self.assertEqual(self.monte_cristo.num_chapters, 60)

      def test_monte_cristo_last_chapter(self):
          self.assertEqual(self.monte_cristo.content_chapters[60-1].split('</title>')[
                     0], '          <title>            <p>XX</p>            <p>ПЯТОЕ ОКТЯБРЯ</p>          ')

      def test_little_prince_number_of_chapters(self):
          self.assertEqual(self.little_prince.num_chapters, 28)

      def test_little_prince_last_chapter(self):
          self.assertEqual(self.little_prince.content_chapters[28-1].split('</title>')[0], '<title><p>XXVII</p>')

      def test_muuuuur_number_of_chapters(self):
          self.assertEqual(self.mur_chant.num_chapters, 5)

      def test_muuuur_last_chapter(self):
          self.assertEqual(self.mur_chant.content_chapters[5-1].split('</title>')[0], '<title><p>Глава пятая</p>')

      def test_bulgakov_tokenizer(self):
          self.assertEqual(len(self.bulgakov.tokenize(2)), 2682)

      def test_little_prince_tokenizer(self):
          self.assertEqual(len(self.little_prince.tokenize(2)),221)

      def test_monte_cristo_tokenizer(self):
          self.assertEqual(len(self.monte_cristo.tokenize(2)), 942)

      def test_muuuur_tokenizer(self):
           self.assertEqual(len(self.mur_chant.tokenize(2)), 1387)

      def test_bulgakov_translator(self):
          self.assertEqual(list(self.bulgakov.translator(1, 'en').items())[19][1], 'atheism')

      def test_monte_cristo_translator(self):
          self.assertEqual(list(self.monte_cristo.translator(1, 'en').items())[7][1], 'baron')

      def test_muur_translator(self):
          self.assertEqual(list(self.mur_chant.translator(1, 'en').items())[3][1], 'basics')

      def test_little_prince_translator(self):
          self.assertEqual(list(self.little_prince.translator(1, 'en').items())[3][1],  'was')