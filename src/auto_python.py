# ./src/auto_python.py
import os
import subprocess
import sys
from io import StringIO
from dotenv import load_dotenv
import re

from langchain.agents import initialize_agent
from langchain.agents.tools import Tool
from langchain.llms import OpenAI
# from langchain.serpapi import SerpAPIWrapper
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.utilities import BashProcess


class TypeScriptREPL:
    def run(self, command: str) -> str:
        try:
            result = subprocess.run(
                ["npx",
                 "ts-node",
                 "-e",
                 command],
                capture_output=True,

                text=True,
                # shell=True
            )
            output = result.stdout
        except Exception as e:
            output = str(e)

        return output


class FileUpdater:
    def run(self, command: str) -> str:
        pattern = r"^file_path: (.+)\nfile_content: ([\s\S]+)$"
        match = re.search(pattern, command)
        if match:
            file_path = match.group(1)
            file_content = match.group(2)
            file_dir = os.path.dirname(file_path)
            try:
                if file_dir != '' and not os.path.exists(file_dir):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(file_content)
                return "File updated"
            except Exception as e:
                return str(e)
        else:
            return f"Invalid command. Command should be in the format: '{pattern}'"  # . We need '\n' between file_path and file_content."


class FileAppender:
    def run(self, command: str) -> str:
        pattern = r"^file_path: (.+)\nfile_content: ([\s\S]+)$"
        match = re.search(pattern, command)
        if match:
            file_path = match.group(1)
            file_content = match.group(2)
            file_dir = os.path.dirname(file_path)
            try:
                if file_dir != '' and not os.path.exists(file_dir):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "a") as f:
                    f.write(file_content)
                return "File updated"
            except Exception as e:
                return str(e)
        else:
            return f"Invalid command. Command should be in the format: '{pattern}'"


class PythonREPL:
    def run(self, command: str) -> str:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals())
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output


load_dotenv()

llm = OpenAI(
    temperature=0.0,
    # openai_api_key=os.getenv("OPENAI_API_KEY"),
)
python_repl = Tool("Python REPL",
                   PythonREPL().run,
                   """A Python Sell. Use this to execute python commands. Input should be a valid python command. 
                   For example, "print('Hello, World!')" will print "Hello, World!" to the console.
                   If you expect output it should be printed out.""")
# type_script_repl = Tool("TypeScript REPL",
#                         TypeScriptREPL().run,
#                         """A TypeScript Shell. Use this to execute TypeScript commands. Input should be a valid TypeScript command.
#                         For example, "console.log('Hello, World!')" will print "Hello, World!" to the console.
#                         If you expect output it should be printed out.""")
type_script_repl = Tool("TypeScript REPL",
                        TypeScriptREPL().run,
                        """A TypeScript Shell. Use this to execute TypeScript commands. Input should be a valid TypeScript command.
                        For example, "console.log('Hello, World!')" will print "Hello, World!" to the console.
                        If you expect output it should be printed out.""")
search = Tool("Google Search",
              GoogleSearchAPIWrapper().run,
              """useful for when you need to ask with search.""")
file_updator = Tool("File Updator",
                    FileUpdater().run,
                    """useful for when you need to create or update a file.
                    Input should be in the format: 'file_path: <file_path>\\nfile_content: <file_content>'.
                    """)
file_appender = Tool("File Appender",
                     FileUpdater().run,
                     """useful for when you need to create a file or append the content to the file.
                     Input should be in the format: 'file_path: <file_path>\\nfile_content: <file_content>'.
                     """)

bash = Tool("Bash",
            BashProcess().run,
            """useful for when you need to execute bash commands.
            Input should be only command.
            """)
tools = [
    search,
    python_repl,
    type_script_repl,
    file_updator,
    file_appender,
]
agent = initialize_agent(tools, llm,
                         # agent="zero-shot-react-description",
                         # agent=AgentType.SELF_ASK_WITH_SEARCH,
                         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         verbose=True)

# question = "Create simple text file to current path as test.txt. Content is 'Hello World✨'"
questionTypeScript = "Create TypeScript file to output fibonacci number at parameter index and save the program to test.ts."
question = """
# Task steps
1. Research and write a README about langchain.
2. Save the document to ./ABOUT_LANGCHAIN.md.
3. Translate the document to Japanese.
4. Save the document in Japanese to ./ABOUT_LANGCHAIN.ja.md.

"""
queryTemplateRepository = """
Create a MySQLUserRepository class that implements UserRepository interface.
Create unit test for MySQLUserRepository class.

File path of MySQLStatusRepository class is ./src/adapter/repositories/MySQLUserRepository.ts
File path of MySQLRepository class is ./src/domain/usecases/adapter-interfaces/repositories/UserRepository.ts
"""
agent.run("What is my current files?")
# agent.run(questionTypeScript)
# agent.run("What is the 10th fibonacci number?")
