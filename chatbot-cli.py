#!/usr/bin/env python3

import sys, os, os.path, base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import argparse

def _parse_args():
    ap = argparse.ArgumentParser(sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--clientid", "-c",  help="-c <client-id>", required=True, nargs=1)
    return ap.parse_args()

args = _parse_args()

endpoint = os.getenv("ENDPOINT_URL", "https://eastus.api.cognitive.microsoft.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(managed_identity_client_id=args.clientid[0]),  
    "https://cognitiveservices.azure.com/.default"  
)

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version="2024-05-01-preview",  
)  

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model = "gpt-35-turbo",
        messages = [{"role": "user", "content": prompt}]
    )

    return(response.choices[0].message.content.strip())

if __name__ == "__main__":
    while True:
        user_input = input("Ask a question: ")
        if user_input.lower() in ["quit","q"]:
            break
        
        response = chat_with_gpt(user_input)
        sys.stdout.write("OpenAI: {}\n\n".format(response))

