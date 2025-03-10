# Cold Email Generator using Gen AI

An AI-powered tool that generates personalized cold emails for job applications. The tool scrapes job listings from a provided careers page URL, extracts key job details using a Mistral-7B-Instruct model via the Hugging Face API, and augments the email with relevant portfolio links retrieved from a CSV-based vector database using ChromaDB.

---

## Features

- **Job Listing Extraction:** Scrapes job postings from a careers page.
- **AI-Powered Parsing:** Extracts job details such as role, experience, skills, and description.
- **Personalized Email Generation:** Creates tailored cold emails for job applications.
- **Portfolio Integration:** Retrieves portfolio links based on required skills.
- **Interactive UI:** Built with Streamlit for user-friendly interaction.

---

## Technologies Used

- LangChain
- Mistral-7B-Instruct (via Hugging Face API)
- ChromaDB
- Streamlit
- Pandas
- BeautifulSoup or Scrapy

---

## Setup & Installation

1. **Clone the Repository:**  
   Clone the repository from GitHub and navigate into the project folder.

2. **Virtual Environment:**  
   Create and activate a Python virtual environment.

3. **Install Dependencies:**  
   Install all required dependencies listed in the `requirements.txt` file.

4. **Configure Environment Variables:**  
   Create a `.env` file in the project root and add your Hugging Face API key.

5. **Run the Application:**  
   Launch the application using Streamlit to open the web-based user interface.

---

## Usage

- Enter a careers page URL in the provided text field.
- The application scrapes the job listings, extracts job details, and generates personalized cold emails.
- The generated emails include relevant portfolio links and are displayed on the interface.

---

## License

This project is licensed under the MIT License.

---

Feel free to modify and expand this README as your project evolves. Happy coding!
