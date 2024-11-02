import unittest
from unittest.mock import patch, Mock
from src.app import app


class TranslationRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.utils.huggingface.requests.post')
    def test_translate(self, mock_post):
        mock_response_zh_en = Mock()
        mock_response_zh_en.status_code = 200
        mock_response_zh_en.json.return_value = [{'translation_text': 'hello'}]

        mock_response_en_uk = Mock()
        mock_response_en_uk.status_code = 200
        mock_response_en_uk.json.return_value = [{'translation_text': 'привіт'}]

        mock_post.side_effect = [mock_response_zh_en, mock_response_en_uk]

        response = self.app.post('/api/translate/generate-translate', json={'chinese_word': '你好'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('translation', response.get_json())
        self.assertIn('individual_translations', response.get_json())

    @patch('src.utils.huggingface.requests.post')
    def test_translate_failed(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        mock_post.return_value = mock_response

        response = self.app.post('/api/translate/generate-translate', json={'chinese_word': '你好'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to translate', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
