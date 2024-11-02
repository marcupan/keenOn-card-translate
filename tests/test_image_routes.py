import unittest
from unittest.mock import patch, Mock
from src.app import app


class ImageRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.utils.huggingface.requests.post')
    def test_generate_image_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'\x89PNG\r\n\x1a\n'
        mock_post.return_value = mock_response

        response = self.app.post('/api/image/generate', json={'prompt': 'A beautiful landscape with mountains'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')
        self.assertTrue(len(response.data) > 0)

    @patch('src.utils.huggingface.requests.post')
    def test_generate_image_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        response = self.app.post('/api/image/generate', json={'prompt': 'A beautiful landscape with mountains'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('Failed to generate image', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
