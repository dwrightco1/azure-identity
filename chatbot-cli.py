#!/usr/bin/env python3

import sys, os, os.path, base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import argparse
from pprint import pprint

# ./chatbot-cli.py -c 6dc22f88-e3c6-4e28-9318-0b4b20c0d746 -e https://eastus.api.cognitive.microsoft.com/ -a 2024-05-01-preview -d gpt-35-turbo

def _parse_args():
    ap = argparse.ArgumentParser(sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--clientid", "-c",  help="-c <client-id>", required=True, nargs=1)
    ap.add_argument("--endpointurl", "-e",  help="-e <endpoint-url>", required=True, nargs=1)
    ap.add_argument("--apiversion", "-a",  help="-a <api-version>", required=True, nargs=1)
    ap.add_argument("--deployment", "-d",  help="-d <deployment>", required=True, nargs=1)
    return ap.parse_args()

args = _parse_args()

token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(managed_identity_client_id=args.clientid[0]),  
    #DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"  
)

pprint(vars(token_provider))

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
    azure_endpoint=args.endpointurl[0],  
    azure_ad_token_provider=token_provider,  
    api_version=args.apiversion[0],
)  

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model = args.deployment[0],
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

