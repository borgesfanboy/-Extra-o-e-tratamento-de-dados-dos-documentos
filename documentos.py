#instale todas as bibliotecas :)
import os
import PyPDF2 
import docx 
import faiss # vou deixar o comnando de instalação = pip install faiss-cpu
import numpy as np
from sentence_transformers import SentenceTransformer



def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = pypdf2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file_path)
        else:
            continue
        documents.append((filename, text))
    return documents


def generate_embeddings(texts, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    return embeddings


def create_faiss_index(embeddings, dimension=384):
    index = faiss.IndexFlatL2(dimension) 
    return index

def process_documents(folder_path):
    
    documents = load_documents(folder_path)
    
    
    filenames = [doc[0] for doc in documents]
    texts = [doc[1] for doc in documents]
    
   
    embeddings = generate_embeddings(texts)
    
   
    index = create_faiss_index(np.array(embeddings))
    
    return index, filenames

# Exemplo de uso :)
folder_path = "C:\\Users\\visitante\\Downloads\\meu_arquivo.pdf" 
index, filenames = process_documents(folder_path)

# Consulta exemplo: você pode pesquisar documentos similares a uma nova entrada de texto
query_text = "Exemplo de texto de consulta"
query_embedding = generate_embeddings([query_text])[0]


D, I = index.search(np.array([query_embedding]), k=5) 


print("Documentos mais similares:")
for i in range(len(I[0])):
    print(f"Documento: {filenames[I[0][i]]}, Similaridade: {D[0][i]}")