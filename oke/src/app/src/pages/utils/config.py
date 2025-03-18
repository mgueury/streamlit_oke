# config.py
# Author: Ansh

DB_TYPE = "qdrant"  # Options: "oracle", "qdrant"

# OracleDB Configuration
ORACLE_DB_USER = "##TF_VAR_db_user##"  #Enter your oracle vector Db username
ORACLE_DB_PWD = "##TF_VAR_db_password##"  #Enter your oracle vector Db password
ORACLE_DB_HOST_IP = "XXXXX"  #Enter your oracle vector Db host ip
ORACLE_DB_PORT = 1521   #Enter your oracle vector Db host port
ORACLE_DB_SERVICE = "##DB_URL##" 

ORACLE_USERNAME = ORACLE_DB_USER
ORACLE_PASSWORD = ORACLE_DB_PWD
ORACLE_DSN = f"{ORACLE_DB_HOST_IP}:{ORACLE_DB_PORT}/{ORACLE_DB_SERVICE}"
ORACLE_TABLE_NAME = "policyTable" #name of table where you want to store the embeddings in oracle DB

# Qdrant Configuration
QDRANT_LOCATION = ":memory:"
QDRANT_COLLECTION_NAME = "my_documents" #name of table where you want to store the embeddings in qdrant DB
QDRANT_DISTANCE_FUNC = "Dot"

# Common Configuration
COMPARTMENT_ID = "##TF_VAR_compartment_ocid##"
OBJECT_STORAGE_LINK = "https://objectstorage.##TF_VAR_region##.oraclecloud.com/n/xxxxx/b/xxxxxx/o/"
DIRECTORY = 'data'  # directory to store the pdf's from where the RAG model should take the documents from
PROMPT_CONTEXT = "You are an AI Assistant trained to give answers based only on the information provided. Given only the above text provided and not prior knowledge, answer the query. If someone asks you a question and you don't know the answer, don't try to make up a response, simply say: I don't know."
ENDPOINT= "https://inference.generativeai.##TF_VAR_region##.oci.oraclecloud.com" #change in case you want to select a diff region
EMBEDDING_MODEL = "cohere.embed-multilingual-v3.0"
GENERATE_MODEL = "cohere.command-r-plus-08-2024"  # cohere.command-r-16k or cohere.command-r-plus