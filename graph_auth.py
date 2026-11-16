#!/usr/bin/env python3
# graph_auth.py - get a Graph token with client credentials and print its claims

# 1. imports
from dotenv import load_dotenv
import os
import sys
# 2. load .env and read TENANT_ID, CLIENT_ID, CLIENT_SECRET (fail clearly if missing)
load_dotenv()
try:
    tenant_id=os.environ["TENANT_ID"]
    client_id=os.environ["CLIENT_ID"]
    client_secret=os.environ["CLIENT_SECRET"]
except KeyError as e:
    print(f"no value in .env for {e}")
    sys.exit(1)
print(tenant_id)
print(client_id)
print(len(client_secret))

# 3. build the confidential client (authority = login URL + tenant)

# 4. request a token for scope https://graph.microsoft.com/.default

# 5. if no access_token in the result: print the error, exit non-zero

# 6. decode the middle segment of the token (add padding) and print the claims as JSON
