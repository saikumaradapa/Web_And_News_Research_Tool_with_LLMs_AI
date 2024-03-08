import requests
from bs4 import BeautifulSoup
import streamlit as st
import os
from langchain.llms import GooglePalm
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize GooglePalm and HuggingFace embeddings
llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.7)
instructor_embeddings = HuggingFaceEmbeddings()
main_placeholder = st.empty()

# File paths
vectordb_file_path = "faiss_index_webs"
extracted_filename = "extracted_data.txt"

# Function to extract text and create a vector database
def create_vector_db(urls):
    with open(extracted_filename, "w", encoding="utf-8") as file:
        # Check if the file already exists
        if os.path.exists(vectordb_file_path):
            main_placeholder.text("Data Base Already Existed...✅✅✅")
            print(f"Vector database file '{vectordb_file_path}' already exists. Skipping creation.")
            return

        main_placeholder.text("Data Loading...Started...✅✅✅")
        data = ""
        for url in urls:
            try:
                # Adjust headers as needed, e.g., 'User-Agent' and 'Accept'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                file.write(soup.get_text())
                data = data + "\n\n\n" + soup.get_text()
            except requests.exceptions.HTTPError as errh:
                print ("HTTP Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something went wrong",err)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_text(data)

        # Create FAISS vector database
        main_placeholder.text("Data Base Creation...Started...✅✅✅")
        vectordb = FAISS.from_texts(texts=docs, embedding=instructor_embeddings)
        vectordb.save_local(vectordb_file_path)

        print(f"Vector database created and saved at '{vectordb_file_path}'.")
        main_placeholder.text("Data Base Creation...Done...✅✅✅")

# Function to get the answer using the RetrievalQA chain
def get_answer(query):
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the provided context and a question, generate an answer based solely on the information within this context. 
    Aim to incorporate as much relevant text and in natural language according to question asked from the given source document context into your answer. 
    If the answer cannot be located within the provided context, please explicitly state "No data provided in websites." Avoid fabricating an answer.


        CONTEXT: {context}

        QUESTION: {question}"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                        input_key="query", return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain(query)["result"]

# Streamlit UI
st.title("TeckyBot: Web Research Tool 📈")
st.sidebar.title("News Article / Web URLs")
main_placeholder = st.empty()

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
st.sidebar.write("TeckyBot is a News/ Web Research Tool designed to assist users in extracting information and generating answers from provided URLs. \n\n Developed by    --   '[Sai Kumar Adapa](https://www.linkedin.com/in/sai-kumar-adapa-5a16b2228/)'")
if process_url_clicked:
    create_vector_db(urls)
    st.write("URLs processed successfully!")

query = st.text_area("Enter your query:")

# Button to get the answer
get_answer_clicked = st.button("Get Answer")
if get_answer_clicked:
    if query:
        main_placeholder.text("Searching for answer...😇😇😇")
        answer = get_answer(query)
        st.write(answer)
        main_placeholder.text("I got it...✅✅✅")
    else:
        main_placeholder.text("Please enter a query to get an answer... 👽👽")
