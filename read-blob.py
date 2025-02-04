#!/usr/bin/env python3

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os, sys
import argparse

def _parse_args():
    ap = argparse.ArgumentParser(sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--clientid", "-c",  help="-c <client-id>", required=True, nargs=1)
    ap.add_argument("--storageaccounturl", "-s",  help="-s <storageaccount-url>", required=True, nargs=1)
    ap.add_argument("--blobname", "-b",  help="-b <blob-name>", required=True, nargs=1)
    ap.add_argument("--filename", "-f",  help="-f <filename>", required=True, nargs=1)
    return ap.parse_args()

args = _parse_args()

# Specify the Client ID if using user-assigned managed identities
credential = DefaultAzureCredential(managed_identity_client_id=args.clientid[0])
blob_service_client = BlobServiceClient(account_url=args.storageaccounturl[0], credential=credential)
container_client = blob_service_client.get_container_client(args.blobname[0])
blob_client = container_client.get_blob_client(args.filename[0])

def download_blob():
    if blob_client.exists():
        download_stream = blob_client.download_blob()
        blob_contents = download_stream.readall().decode('utf-8')
        print("Downloaded blob content:", blob_contents)

download_blob()
