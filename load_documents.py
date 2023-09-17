from llama_index import Document
from llama_index.schema import MetadataMode

ACT_METADATA = {
  "act_1": {
    "act": 1,
    "documents_path": "./documents/quests/act_1",
    "description": "This document includes quests and progressions in Baldur's Gate 3's Act 1."
  },
  "act_2": {
    "act": 2,
    "documents_path": "./documents/quests/act_2",
    "description": "This document includes quests and progressions in Baldur's Gate 3's Act 2."
  },
  "act_3": {
    "act": 3,
    "documents_path": "./documents/quests/act_3",
    "description": "This document includes quests and progressions in Baldur's Gate 3's Act 3."
  }
}

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