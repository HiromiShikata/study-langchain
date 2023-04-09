# ./tests/test_openai_client.py

import unittest
from unittest.mock import MagicMock, patch
from src.openai_client import OpenAIClient

class TestOpenAIClient(unittest.TestCase):

    def setUp(self):
        self.client = OpenAIClient()

    def test_generate_text(self):
        with patch('src.openai_client.OpenAI') as mock_openai:
            mock_openai_instance = MagicMock()
            mock_openai.return_value = mock_openai_instance
            mock_openai_instance.__call__.return_value = 'Generated text'

            prompt = 'Please generate some text.'
            result = self.client.generate_text(prompt)

            mock_openai.assert_called_once()
            mock_openai_instance.__call__.assert_called_once_with(prompt)
            self.assertEqual(result, 'Generated text')

    def test_generate_text_no_mock(self):
        prompt = 'Please generate some text.'
        result = self.client.generate_text(prompt)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_generate_unittest(self):
        with patch('src.openai_client.OpenAI') as mock_openai, \
                patch('src.openai_client.PromptTemplate') as mock_prompt_template, \
                patch('src.openai_client.LLMChain') as mock_llm_chain:

            mock_openai_instance = MagicMock()
            mock_openai.return_value = mock_openai_instance

            mock_prompt_template_instance = MagicMock()
            mock_prompt_template.return_value = mock_prompt_template_instance

            mock_llm_chain_instance = MagicMock()
            mock_llm_chain.return_value = mock_llm_chain_instance
            mock_llm_chain_instance.run.return_value = 'Generated unit test'

            target_file_path = 'target_file.py'
            test_file_path = 'test_target_file.py'
            related_file_contents = 'Related file contents'

            result = self.client.generate_unittest(target_file_path, test_file_path, related_file_contents)

            mock_openai.assert_called_once()
            mock_prompt_template.assert_called_once_with(input_variables=["target_file_path", "test_file_path", "related_file_contents"],
                                                         template=unittest.mock.ANY)
            mock_llm_chain.assert_called_once_with(llm=mock_openai_instance, prompt=mock_prompt_template_instance)

            self.assertEqual(result, 'Generated unit test')

    def test_generate_unittest_no_mock(self):
        target_file_path = 'target_file.py'
        test_file_path = 'test_target_file.py'
        related_file_contents = 'Related file contents'

        result = self.client.generate_unittest(target_file_path, test_file_path, related_file_contents)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
