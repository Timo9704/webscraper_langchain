import os
import random
from time import sleep

from dotenv import load_dotenv
from langchain_community.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from webscraper_planner_plants.scraper_aquaristikprofi import extract_aquaristikprofi_content
from webscraper_planner_plants.scraper_drta import extract_drta_content
from webscraper_planner_plants.scraper_megazoo import extract_megazoo_content
from webscraper_planner_plants.scraper_tropica import extract_tropica_content
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

load_dotenv()
llm = ChatOpenAI(temperature=0)

def read_urls_from_directory(directory_path):
    urls = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                urls.extend(file.read().splitlines())
    return urls


def split_to_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o-mini", chunk_size=400, chunk_overlap=10
    )
    splits = text_splitter.split_text(text)
    return splits


def upload_to_vectordatabase_plants(splittedfiles):
    embedding = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index("aiplannerplants", embedding=embedding)
    vectorstore.add_texts(splittedfiles)


def upload_to_vectordatabase_fishes(splittedfiles):
    embedding = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index("aiplannerfishes", embedding=embedding)
    vectorstore.add_texts(splittedfiles)

def upload_to_vectordatabase_aquarium(splittedfiles):
    embedding = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index("aiplanneraquarium", embedding=embedding)
    vectorstore.add_texts(splittedfiles)

def restructure_content_aquarium(text):
    prompt = "Fasse diesen Text in vier Abschnitten strukturiert zusammen: 1. Technische Daten des Aquariums (Name des Herstellers, Name des Aquarium oder Modellname, Liter, Länge des Aquariums, Unterschrank: ja oder nein?, als Set: ja oder nein? - ja, nur wenn Technik mit dabei ist), 2. Inkludierte Technik oder Zubehör (Modellname, Watt, Lumen, Durchflussmenge), 3. Preis des Aquariums 4. Weitere Besonderheiten des Aquariums"
    return llm.invoke(prompt + str(text)).content

def clean_recreate_index():
    # Delete and recreate existing index
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    pc.delete_index("aiplannerplants")
    pc.delete_index("aiplannerfishes")
    pc.delete_index("aiplanneraquarium")
    pc.create_index(name="aiplannerplants", dimension=1536, metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    pc.create_index(name="aiplannerfishes", dimension=1536, metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    pc.create_index(name="aiplanneraquarium", dimension=1536, metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))

def main(file_path):
    urls = read_urls_from_directory(file_path)
    # Extract content from URL + sleep for sustainable scraping
    sleep(random.randint(5, 10))
    load_dotenv()

    clean_recreate_index()

    for url in urls:

        if "tropica" in url:
            splittedcontent = split_to_chunks(extract_tropica_content(url))
            upload_to_vectordatabase_plants(splittedcontent)
        if "drta" in url:
            splittedcontent = split_to_chunks(extract_drta_content(url))
            upload_to_vectordatabase_fishes(splittedcontent)
        if "aquaristik-profi" in url:
            splittedcontent = split_to_chunks(extract_aquaristikprofi_content(url))
            upload_to_vectordatabase_fishes(splittedcontent)
        if "megazoo" in url:
            sleep(3)
            restructured = restructure_content_aquarium(extract_megazoo_content(url))
            splittedcontent = split_to_chunks(restructured)
            upload_to_vectordatabase_aquarium(splittedcontent)

        print("Successfully uploaded content of " + url)


if __name__ == '__main__':
    # Pfad zur Datei mit den URLs
    file_path = './sources/'
    main(file_path)
