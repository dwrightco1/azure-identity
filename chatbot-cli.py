#!/bin/env python3

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import sys, os, os.path, base64
from openai import AzureOpenAI
import argparse

subscription_key = ""

def _parse_args():
    ap = argparse.ArgumentParser(sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--clientid", "-c",  help="-c <client-id>", required=True, nargs=1)
    ap.add_argument("--vault", "-v",  help="-v <vault-url>", required=True, nargs=1)
    ap.add_argument("--secret", "-s",  help="-s <secret-name>", required=True, nargs=1)
    ap.add_argument("--endpointurl", "-e",  help="-e <endpoint-url>", required=True, nargs=1)
    ap.add_argument("--apiversion", "-a",  help="-a <api-version>", required=True, nargs=1)
    ap.add_argument("--deployment", "-d",  help="-d <deployment>", required=True, nargs=1)
    return ap.parse_args()

def get_secret():
    credential = DefaultAzureCredential(managed_identity_client_id=args.clientid[0])
    client = SecretClient(vault_url=args.vault[0], credential=credential)
    secret = client.get_secret(args.secret[0])
    return(secret.value)

args = _parse_args()


# Initialize OpenAI session
client = AzureOpenAI(
    azure_endpoint=args.endpointurl[0],
    api_key=subscription_key,
    api_version=args.apiversion[0],
)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model = args.deployment[0],
        messages = [{"role": "user", "content": prompt}]
    )

    return(response.choices[0].message.content.strip())

if __name__ == "__main__":
    # Start chatbot prompt loop
    subscription_key = get_secret()
    while True:
        user_input = input("Ask a question: ")
        if user_input.lower() in ["quit","q"]:
            break
        
        response = chat_with_gpt(user_input)
        sys.stdout.write("OpenAI: {}\n\n".format(response))

