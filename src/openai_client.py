# ./src/openai_client.py

import argparse
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class OpenAIClient:
    def __init__(self):
        pass

    def generate_text(self, prompt):
        llm = OpenAI()
        res = llm(prompt)
        print(res)
        return res

    def generate_unittest(self, target_file_path, test_file_path, related_file_contents):
        template = """
        Please write a unit test for the following file::
        
        # Target file path
        {target_file_path}
        
        # Test file path
        {test_file_path}

        # Related file contents
        {related_file_contents}
        """
        prompt = PromptTemplate(
            input_variables=["target_file_path","test_file_path","related_file_contents"],
            template=template)
        llm = OpenAI()
        # print(target_file_path)
        # print(test_file_path)
        # print(related_file_contents)
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run({
            "target_file_path": target_file_path,
            "test_file_path": test_file_path,
            "related_file_contents": related_file_contents})
        print(response.strip())
        return response.strip()

def main():
    parser = argparse.ArgumentParser(description='OpenAI Client')
    parser.add_argument('--target_file_path', type=str, help='Target file path')
    parser.add_argument('--test_file_path', type=str, help='Test file path')
    parser.add_argument('--related_file_contents', type=str, help='Related file contents')
    args = parser.parse_args()

    client = OpenAIClient()
    client.generate_unittest(args.target_file_path, args.test_file_path, args.related_file_contents)

if __name__ == '__main__':
    main()
