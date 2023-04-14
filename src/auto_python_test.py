import unittest
from io import StringIO
from unittest.mock import MagicMock, patch
from src.auto_python import PythonREPL, agent

# class TestPythonREPL(unittest.TestCase):
    def setUp(self):
        self.python_repl = PythonREPL()

    def test_run_valid_command(self):
        command = "print('Hello, World!')"
        expected_output = "Hello, World!\n"
        self.assertEqual(self.python_repl.run(command), expected_output)

    def test_run_invalid_command(self):
        command = "printt('Hello, World!')"
        expected_output = "name 'printt' is not defined"
        self.assertTrue(expected_output in self.python_repl.run(command))

class TestAgent(unittest.TestCase):
    def test_agent_run(self):
        with patch("langchain.agents.initialize_agent") as mock_agent:
            mock_run = MagicMock()
            mock_run.return_value = "55"
            mock_agent_instance = MagicMock()
            mock_agent_instance.run = mock_run
            mock_agent.return_value = mock_agent_instance

            question = "Create TypeScript file to output fibonacci number at parameter index."
            expected_answer = "55"
            self.assertEqual(agent.run(question), expected_answer)

if __name__ == '__main__':
    unittest.main()
