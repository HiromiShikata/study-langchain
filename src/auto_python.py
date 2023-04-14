# ./src/auto_python.py
import os
import subprocess
import sys
from io import StringIO


from langchain.agents import initialize_agent
from langchain.agents.tools import Tool
from langchain.llms import OpenAI
from langchain.serpapi import SerpAPIWrapper
from langchain.agents.agent_types import AgentType


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


class OldTypeScriptREPL:
    def run(self, command: str) -> str:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        try:
            read_stdout, write_stdout = os.pipe()
            read_stderr, write_stderr = os.pipe()

            result = subprocess.run(
                ['npx', 'tsun', '-e', command],
                stdout=write_stdout,
                stderr=write_stderr,
                text=True,
                check=True
            )

            os.close(write_stdout)
            os.close(write_stderr)

            with open(read_stdout) as stdout_file:
                stdout_output = stdout_file.read()
            with open(read_stderr) as stderr_file:
                stderr_output = stderr_file.read()

            sys.stdout = old_stdout
            output = mystdout.getvalue() + stdout_output

        except subprocess.CalledProcessError as e:
            sys.stdout = old_stdout
            output = mystdout.getvalue() + stderr_output

        return output


llm = OpenAI(temperature=0.0)
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
search = Tool("Intermediate Answer",
              SerpAPIWrapper().run,
              """useful for when you need to ask with search.""")

tools = [search, python_repl, type_script_repl]
agent = initialize_agent(tools, llm,
                         # agent="zero-shot-react-description",
                         agent=AgentType.SELF_ASK_WITH_SEARCH,
                         verbose=True)

question = "Create TypeScript file to output fibonacci number at parameter index."
agent.run(question)
# agent.run("What is the 10th fibonacci number?")
