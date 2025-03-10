import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Email Generator")

    # User input for the job URL
    url_input = st.text_input("Enter a Careers Page URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load job listing content from the given URL
            loader = WebBaseLoader(url_input)
            loaded_data = loader.load()

            if not loaded_data:
                st.error("❌ Failed to retrieve job listings. Please check the URL.")
                return

            raw_page_content = loaded_data.pop().page_content
            cleaned_data = clean_text(raw_page_content)

            if not cleaned_data.strip():
                st.error("❌ Extracted content is empty. Try another URL.")
                return

            # Load portfolio data (if not already loaded)
            portfolio.load_portfolio()

            # Extract job details
            jobs = llm.extract_jobs(cleaned_data)

            if not jobs:
                st.error("❌ No jobs found in the extracted data.")
                return

            # Generate emails for extracted jobs
            for job in jobs:
                skills = job.get('skills', "")

                # Ensure skills are a string
                if isinstance(skills, list):
                    skills = ", ".join(skills)

                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)

                # Display generated email
                st.subheader(f"📨 Cold Email for {job.get('role', 'Unknown Role')}")
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"❌ An Error Occurred: {str(e)}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
