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
