# study-langchain

The OpenAI Client is a command-line tool that provides a simple interface to generate text using OpenAI's GPT language model. It includes two main functions: `generate_text` and `generate_unittest`.

## Installation

The OpenAI Client requires Python 3.6 or higher. To install the necessary dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage

### generate_text

The `generate_text` function generates text based on a prompt provided as an argument. To use this function, import the `OpenAIClient` class from the `openai_client.py` module and create an instance of it. Then, call the `generate_text` function with a prompt as the argument.

```python
from openai_client import OpenAIClient

client = OpenAIClient()
client.generate_text("This is a prompt.")
```

### generate_unittest

The `generate_unittest` function generates a unit test based on a target file path, test file path, and related file contents provided as arguments. To use this function, import the `OpenAIClient` class from the `openai_client.py` module and create an instance of it. Then, call the `generate_unittest` function with the target file path, test file path, and related file contents as arguments.

```python
from openai_client import OpenAIClient

client = OpenAIClient()
client.generate_unittest("target_file.py", "test_file.py", "Related file contents.")
```

### Command Line Interface

The OpenAI Client can also be used from the command line. To generate a unit test, run the following command:

```
python openai_client.py --target_file_path target_file.py --test_file_path test_file.py --related_file_contents "Related file contents."
```

## License

The OpenAI Client is licensed under the [MIT License](https://opensource.org/licenses/MIT).
