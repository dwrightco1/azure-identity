# Sample Code for Using Managed Identities
The sample code in this directory provides Python-based examples for using Azure Managed Identities for access various types of Azure resoruces

For reference, see [this link](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview-for-developers?tabs=python).

##### Configure Python Virtual Environment
Before you can run any of the sample applications, you'll need to configure a Python Virtual Environment with the required libraries from the Azure SDK:
```
python3 -m venv ~/venv-mid
. ~/venv-mid/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

##### Key Vault Access
```
./read-secret.py -c <mid-clientid> -v <keyvault-url> -s <secret-name>
```

##### Blob Access
```
./read-blob.py -c <clientid> -s <storageaccount-url> -b <blob-name> -f <filename>
```

##### Demonstrate using the managed identity to authenticate to OpenAI (by reading accesskey from key vault)
```
./chatbot-cli.py -c <mid-clientid> -v <vault-url> -s openai-key -e https://eastus.api.cognitive.microsoft.com/ -a 2024-05-01-preview -d gpt-35-turbo
```

> NOTE: Before running the command above, you'll need to add a vault secret named `openai-key` and initialize its value with the OpenAI access key.

##### Demonstrate using the managed identity to mount a CIFS share from a storage account
```
./mount-storage.sh <mid-clientid> <storageacct-name> <share-name> <pointpoint> <resource-group>
```

> NOTE: You will need to assign the `Contributor` RBAC role on the storage account for the managed identity.
