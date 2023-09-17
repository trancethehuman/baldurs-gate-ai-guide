from llama_index import Document
from llama_index.schema import MetadataMode

document = Document(
    text="This is a super-customized document",
    metadata={
        "file_name": "super_secret_document.txt",
        "category": "finance",
        "author": "LlamaIndex"    
    },
    excluded_llm_metadata_keys=['file_name'],
    metadata_seperator="::",
    metadata_template="{key}=>{value}",
    text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
)

print("The LLM sees this: \n", document.get_content(metadata_mode=MetadataMode.LLM))
print("The Embedding model sees this: \n", document.get_content(metadata_mode=MetadataMode.EMBED))

