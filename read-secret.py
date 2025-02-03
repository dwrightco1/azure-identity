#!/usr/bin/env python3

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os, sys
import argparse

def _parse_args():
    ap = argparse.ArgumentParser(sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--clientid", "-c",  help="-c <client-id>", required=True, nargs=1)
    ap.add_argument("--vault", "-v",  help="-v <vault-url>", required=True, nargs=1)
    ap.add_argument("--secret", "-s",  help="-s <secret-name>", required=True, nargs=1)
    return ap.parse_args()

args = _parse_args()

# Assign vars from commandline arguments
credential = DefaultAzureCredential(managed_identity_client_id=args.clientid[0])
client = SecretClient(vault_url=args.vault[0], credential=credential)

def get_secret():
    secret = client.get_secret(args.secret[0])
    secret_value = secret.value
    sys.stdout.write("secret value = {}\n".format(secret_value))

if __name__ == "__main__":
    try:
        get_secret()
    except Exception as e:
        print(f"Error retrieving secret: {e}")