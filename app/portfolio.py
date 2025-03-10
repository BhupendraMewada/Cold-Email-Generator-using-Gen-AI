import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path

        # Ensure the CSV file exists before reading
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Error: Portfolio CSV file '{file_path}' not found.")

        self.data = pd.read_csv(file_path)

        # Initialize ChromaDB with persistent storage
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """
        Loads portfolio data into ChromaDB if it's empty.
        """
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                # Ensure values are lists before adding to ChromaDB
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )
            print("✅ Portfolio data loaded successfully.")
        else:
            print("⚠️ Portfolio data already exists in ChromaDB.")

    def query_links(self, skills):
        """
        Queries ChromaDB for portfolio links based on skills.

        :param skills: A string containing required skills.
        :return: List of portfolio links (max 2 results).
        """
        results = self.collection.query(query_texts=[skills], n_results=2)

        # Extract links from metadata (handle empty results)
        return [meta["links"] for meta in results.get("metadatas", [{}])[0]] if results.get("metadatas") else []

# Example Usage
if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.load_portfolio()  # Load data if empty

    skills_query = "Python, AI, Machine Learning"
    related_links = portfolio.query_links(skills_query)
    print("🔗 Related Portfolio Links:", related_links)
