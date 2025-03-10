import os
import requests
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")  # Hugging Face API Key
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"  # Lightweight Mistral Model

        if not self.api_key:
            raise ValueError("❌ Hugging Face API Key is missing. Check your .env file.")

    def query_mistral(self, prompt):
        """
        Calls Hugging Face API to generate a response using Mistral-7B-Instruct.
        """
        API_URL = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            raise ValueError(f"❌ API Error {response.status_code}: {response.text}")

    def extract_jobs(self, cleaned_text):
        """
        Extracts job listings from scraped website text using Mistral API.
        """
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            
            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Extract job postings and return them in JSON format with the following keys: 
            - `role`
            - `experience`
            - `skills`
            - `description`

            Only return a valid JSON response without any extra text.

            ### RESPONSE FORMAT:
            ```json
            {{
                "role": "Software Engineer",
                "experience": "3+ years in Python and AI",
                "skills": ["Python", "AI", "Machine Learning"],
                "description": "Develop AI-powered applications using Python."
            }}
            ```
            """
        )

        chain_extract = prompt_extract.format(page_data=cleaned_text)
        response_text = self.query_mistral(chain_extract)

        # Ensure response is valid JSON
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(response_text)
        except OutputParserException:
            raise OutputParserException("❌ Context too big. Unable to parse jobs.")

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        """
        Generates a personalized cold email based on job details.
        """
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are Bhupendra Mewada, an aspiring Data Analyst, Data Scientist, and Gen AI Developer.
        You are writing a cold email to apply for the job mentioned in the URL above.
        Your email should highlight your passion, skills, and experience in data analytics, data science, and generative AI.
        Include the most relevant portfolio links from: {link_list}
        Do NOT provide any preamble.

        ### EMAIL (NO PREAMBLE):
        """
        )


        chain_email = prompt_email.format(job_description=str(job), link_list=links)
        response_text = self.query_mistral(chain_email)

        return response_text  # Return the generated email

if __name__ == "__main__":
    print(os.getenv("HF_API_KEY"))  # Print API Key for Debugging (Ensure it's loaded)
