"""
Configuration for IBM watsonx.ai Telecom Training Assistant
"""

# IBM watsonx.ai credentials
WATSONX_API_KEY = "717qjdpmYKKfz5smjH9CdKB6yTn1jEQ15yKNiopw7LTq"
WATSONX_PROJECT_ID = "597e582f-98a9-422e-9c62-86c7a1c3eb9e"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"

# Model configuration
# granite-4-h-small: IBM Granite 4 (latest instruct model available in this project)
GRANITE_MODEL_ID = "ibm/granite-4-h-small"

# Generation parameters
GENERATE_PARAMS = {
    "max_new_tokens": 512,
    "min_new_tokens": 10,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.1,
}

QUIZ_PARAMS = {
    "max_new_tokens": 900,
    "min_new_tokens": 50,
    "temperature": 0.8,
    "top_p": 0.95,
    "repetition_penalty": 1.1,
}

# RAG configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 4
CHROMA_PERSIST_DIR = "./chroma_db"
