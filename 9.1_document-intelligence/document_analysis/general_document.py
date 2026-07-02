from pathlib import Path
from dotenv import load_dotenv
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOCUMENT_INTELLIGENCE_KEY")


# sample document
formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", formUrl)
result = poller.result()

print("----Key-value pairs found in document----")
for kv_pair in result.key_value_pairs:
    if kv_pair.key and kv_pair.value:
        print("Key '{}': Value: '{}'".format(kv_pair.key.content, kv_pair.value.content))
    else:
        print("Key '{}': Value:".format(kv_pair.key.content))

print("----------------------------------------")