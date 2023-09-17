import os

import chromadb
import openai
from dotenv import load_dotenv
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import (Document, ServiceContext, SimpleDirectoryReader,
                         VectorStoreIndex)
from llama_index.embeddings import LangchainEmbedding, OpenAIEmbedding
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

# define embedding function
embed_model = OpenAIEmbedding(embed_batch_size=10)

node_parser = SimpleNodeParser.from_defaults(chunk_size=1300, chunk_overlap=200)

# load documents
documents = SimpleDirectoryReader(input_dir="./documents/quests/", recursive=True).load_data()

BALDURS_GATE_3_ALL_ACTS_METADATA = [
  {
    "act": 1,
    "documents_path": "./documents/quests/act_1",
    "description": "Tips and guides for Baldur's Gate 3's Act 1."
  },
  {
    "act": 2,
    "documents_path": "./documents/quests/act_2",
    "description": "Tips and guides for Baldur's Gate 3's Act 2."
  },{
    "act": 3,
    "documents_path": "./documents/quests/act_3",
    "description": "Tips and guides for Baldur's Gate 3's Act 3."
  }
]


# Create a new Chroma Database and save to disk
print("Loading or Creating Chroma Database")
db = chromadb.PersistentClient(path="./chroma_db") # This acts as saving and loading (if path exists)
quests_guide_collection = db.get_or_create_collection("baldurs_gate_3_quests_guide")
vector_store = ChromaVectorStore(chroma_collection=quests_guide_collection)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model, node_parser=node_parser)

index = None

# If the vectorstore doesn't have any documents, create a new index
if quests_guide_collection.count() == 0: # This means the Chroma collection (or index) is brand new
  print("Started loading documents using Llama Index")
  documents = []

  for metadata in BALDURS_GATE_3_ALL_ACTS_METADATA:
    file_names_in_directory = []
    
    if "documents_path" in metadata:
          try:
              filenames = os.listdir(metadata["documents_path"]) # Using os.listdir to get a list of all files in the directory
              for filename in filenames:
                  file_names_in_directory.append(filename)
          except FileNotFoundError:
              print(f"Directory '{metadata['documents_path']}' not found.")
              
    for filename in file_names_in_directory:
      with open(metadata["documents_path"] + "/" + filename, 'r') as f:
            text_content = f.read()
            
      document = Document(
        text=text_content,
        metadata={
            "act": metadata["act"],
            "description": metadata["description"],
            "region": filename,
            "document_path": metadata["documents_path"] + "/" + filename,
            "category": "quest",
        },
        excluded_llm_metadata_keys=['document_path'],
        metadata_seperator="::",
        metadata_template="{key}=>{value}",
        text_template="Metadata: {metadata_str}\n-----\nContent: {content}")
      
      documents.append(document)
  print("Finished loading documents using Llama Index")
      
  print("Adding documents to vectorstore")
  index = VectorStoreIndex.from_documents(
      documents, storage_context=storage_context, service_context=service_context
  )

# If the vectorstore has documents, load the existing index
else:
  print("Started loading vectorstore using Llama Index")
  index = VectorStoreIndex.from_vector_store(
      vector_store,
      service_context=service_context,
  )

# Query Data
query_engine = index.as_query_engine(verbose=True, streaming=True)
print("Started querying using Llama Index")

# print(node_parser.get_nodes_from_documents([documents[0]], show_progress=True))

while True:
  user_query = input("Enter your query: ")
  response = query_engine.query(user_query)
  retrieved_nodes = response.source_nodes
  print(response)
  # print(f"\n{response.source_nodes}")