# EBSI Demonstrator Notes and Examples

#### Table of Contents
1. [Overview](#1-overview)
2. [Setup](#2-setup)
3. [API Usage](#3-api-usage)
4. [Sign and Verify Message using EBSI DID  (Python Code)](#4-sign-and-verify-message-using-ebsi-did--python-code)

# 1. Overview

The [EBSI Demonstrator](https://ec.europa.eu/digital-building-blocks/wikis/display/EBSIDOC/Demonstrator) provides access to the live preproduction  instance of [EBSI's API catalogue](https://api.preprod.ebsi.eu/docs/apis). There are 13 APIs in total:

* **Authorisation** EBSI Core Service responsible for issuing Short Term Access Tokens for access to platform services.

* **DID Registry** EBSI Core Service which provides capabilities to resolve EBSI DIDs.

* **Ledger** Use case applications access to all the available blockchain protocol interfaces.

* **Notifications** EBSI Core Service that helps send async or delayed notifications addressed via DID.

* **Proxy Data Hub** EBSI Core Service providing the capability of securely storing data (off chain) controlled by the owner. Data can be private or shared. Designed to ensure [GDPR data compliance is retained](https://ec.europa.eu/digital-building-blocks/wikis/display/EBSIDOC/Proxy+Data+Hub+API) when storing owner related data.

* **Storage** CRUD operations for files in the off-chain distributed storage. Designed for storage of data produced by [APIs and external apps](https://ec.europa.eu/digital-building-blocks/wikis/display/EBSIDOC/Storage+API).

* **Timestamp** EBSI Core Service for generating/linking/verifying timestamps for record keeping purposes.

* **Trusted Apps Registry** Management of trusted EBSI and external applications (authentication, authorisation etc).

* **Trusted Issuers Registry** Generic decentralised registry holding information about trusted issuers, like public information, accreditations and other. All information is stored in the smart contract in form of Attribute envelops (like Verifiable Credentials). 

* **Trusted Ledgers & Smart Contracts Registry** Enables interaction with the Trusted Ledgers & Smart Contracts Registry

* **Trusted Policies Registry** EBSI core service providing access to policies defined in Policies Registry Smart Contract

* **Trusted Schemas Registry** Register new schema, update scheme and read/validate registered schemas.

* **Users Onboarding** EBSI Core Service enabling users (Natural Persons and Legal Entities) to obtain long-term access to the EBSI pre-production network.

# 2. Setup

Interaction with the EBSI Demonstrator is conducted using their CLI tool. Therefore, first clone and build their CLI tool as per the instructions described in the [test-scripts](https://ec.europa.eu/digital-building-blocks/code/projects/EBSI/repos/test-scripts/browse#install) documentation. It's assumed that prerequisite software (yarn, node.js, git) have been installed on the machine already. Commands to clone and build the CLI tool are as follows:

```
git clone https://ec.europa.eu/digital-building-blocks/code/scm/ebsi/test-scripts.git
git checkout staging #The EBSI demonstrator works on the staging branch of code hence the switch here.
cd test-scripts
yarn build
yarn install --ignore-engines #The --ignore-engines flag was used to suppress version number errors with node.js
```

If the above commands are successful, the EBSI CLI Tool can be started using the command:

```
yarn start
````  

The `==>` prompt which should appear in your terminal signifies that the EBSI CLI Tool is awaiting user instructions.

# 3. API Usage

## 3.1. On-boarding

Before interaction with the EBSI APIs can take place, one must 'onboard' with the platform. This involves generating a new DID with associated private key and anchoring this DID to the EBSI platform. 

Follow the [onboarding steps](https://ec.europa.eu/digital-building-blocks/wikis/display/EBSIDOC/Demonstrator#Demonstrator-Onboardingjourney) in the EBSI documentation to onboard onto the EBSI platform. After running the first command `using user ES256K`,  **make sure to save a local copy of the DID document output**. Additionally, when following the step _Collect your jwt token_ later on, save a copy of `myToken` value too (see Section 3.1.2. for further details).

Example DID document output follows:

```
DID Document: 
{"@context":["https://www.w3.org/ns/did/v1","https://w3id.org/security/suites/jws-2020/v1"],"id":"did:ebsi:z22nYGDBybAXDKBbVeY87XpK","verificationMethod":[{"id":"did:ebsi:z22nYGDBybAXDKBbVeY87XpK#keys-1","type":"JsonWebKey2020","controller":"did:ebsi:z22nYGDBybAXDKBbVeY87XpK","publicKeyJwk":{"kty":"EC","crv":"secp256k1","x":"BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I","y":"IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE"}}],"authentication":["did:ebsi:z22nYGDBybAXDKBbVeY87XpK#keys-1"],"assertionMethod":["did:ebsi:z22nYGDBybAXDKBbVeY87XpK#keys-1"]}

privateKeyJwkES256K (base64): eyJrdHkiOiJFQyIsImNydiI6InNlY3AyNTZrMSIsIngiOiJCSEdHTG5QOVlxQVVQMUJzcU1fYjdJTUh1b1dNYzJ4c0RBNjZ4VGZ6ZDdJIiwieSI6IklZLTlWTHAwZUFLN3llODdfNUI4enRoUE8wU3RKZTRIdTRCSGhabHdUS0UiLCJkIjoiZFViSHVzWVdweDBTYVRPY2dudUFSSmE0S2YybGVmWEQzVG1QWEp4RE1JYyJ9

keys (base64): 
W3sidHlwZSI6Ikpzb25XZWJLZXkyMDIwIiwiaWQiOiJkaWQ6ZWJzaTp6MjJuWUdEQnliQVhES0JiVmVZODdYcEsja2V5cy0xIiwiYWxnIjoiRVMyNTZLIiwicHJpdmF0ZUtleUp3ayI6eyJrdHkiOiJFQyIsImNydiI6InNlY3AyNTZrMSIsIngiOiJCSEdHTG5QOVlxQVVQMUJzcU1fYjdJTUh1b1dNYzJ4c0RBNjZ4VGZ6ZDdJIiwieSI6IklZLTlWTHAwZUFLN3llODdfNUI4enRoUE8wU3RKZTRIdTRCSGhabHdUS0UiLCJkIjoiZFViSHVzWVdweDBTYVRPY2dudUFSSmE0S2YybGVmWEQzVG1QWEp4RE1JYyJ9LCJwdWJsaWNLZXlKd2siOnsia3R5IjoiRUMiLCJjcnYiOiJzZWNwMjU2azEiLCJ4IjoiQkhHR0xuUDlZcUFVUDFCc3FNX2I3SU1IdW9XTWMyeHNEQTY2eFRmemQ3SSIsInkiOiJJWS05VkxwMGVBSzd5ZTg3XzVCOHp0aFBPMFN0SmU0SHU0QkhoWmx3VEtFIn19XQ==

User:
{
  "keys": {
    "ES256K": {
      "id": "did:ebsi:z22nYGDBybAXDKBbVeY87XpK#keys-1",
      "privateKeyJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I",
        "y": "IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE",
        "d": "dUbHusYWpx0SaTOcgnuARJa4Kf2lefXD3TmPXJxDMIc"
      },
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I",
        "y": "IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE"
      },
      "privateKeyEncryptionJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I",
        "y": "IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE",
        "d": "dUbHusYWpx0SaTOcgnuARJa4Kf2lefXD3TmPXJxDMIc"
      },
      "publicKeyEncryptionJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I",
        "y": "IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE"
      }
    }
  },
  "privateKeyHex": "0x7546c7bac616a71d1269339c827b804496b829fda579f5c3dd398f5c9c433087",
  "address": "0x5D4852Ef71e4F9dDb922a14a43Ed421a404d748A",
  "did": "did:ebsi:z22nYGDBybAXDKBbVeY87XpK"
}
```

This document output is your EBSI "wallet" and contains the private key which identifies you on the platform (thus should be kept secret in production). The `did:ebsi:z22nYGDBybAXDKBbVeY87XpK` is the unique identifier for this 'wallet' and the entry `"privateKeyJwk": { ... }` is the private key associated with this DID. 

Once the final step of onboarding are complete, the generated DID should be anchored onto the EBSI platform. This can be confirmed by navigating to the following endpoint and specifying a valid DID.

```
https://api.preprod.ebsi.eu/did-registry/v2/identifiers/<enter your DID here>
```

A live example of a valid DID (which differs from the example in this documentation) is viewable as follows: 

https://api.preprod.ebsi.eu/did-registry/v2/identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC 

### 3.1.1. Load an existing DID and Private Key

The private key, token and other variables defined in the EBSI CLI Tool only persist in-memory. Thus, if the CLI Tool is exited, then these variables are deleted. To load an existing DID with associated private key, the following command can be used:

```
yarn start #assumes we exited the EBSI CLI tool and need to start it again
using user ES256K did1 { "kty": "EC", "crv": "secp256k1", "x": "BHGGLnP9YqAUP1BsqM_b7IMHuoWMc2xsDA66xTfzd7I", "y": "IY-9VLp0eAK7ye87_5B8zthPO0StJe4Hu4BHhZlwTKE", "d": "dUbHusYWpx0SaTOcgnuARJa4Kf2lefXD3TmPXJxDMIc" } did:ebsi:z22nYGDBybAXDKBbVeY87XpK
```

Make sure to replace variables `x`, `y` and `d` and the `did:ebsi:<id>` itself with your own values.

### 3.1.2. Re-use an existing JWT token

Interaction with the EBSI platform APIs are done by presenting a bearer token. The steps to request and store a token are done via the following commands as shown in the EBSI documentation:

```
# Get a request from the API
# Start a SIOP authentication with authorisation api. The authorisation api will return a request
==> request: authorisation siopRequest
 
# Verify the request
# Check the signature and did in the request. It return the client_id specified in the request.
==> callbackUrl: compute verifyAuthenticationRequest request
 
# Send a response to the api
# Call /siop-sessions in authorisation api
==> sessionResponse: authorisation siopSession callbackUrl ES256K
 
# Verify the response and get the access token
# Check the nonce and signature in the Ake response. It decrypts and returns the access token contained in the Ake response.
==> myToken: compute verifySessionResponse sessionResponse
 
# Use our JWT access token
==> using token myToken
```

The variable `myToken` is automatically presented to the platform when certain interactions with the API are made. Similar to the DID, this token persists only in-memory and will be deleted if the CLI Tool terminal is exited. If the base64 output string of myToken is saved offline, it can be re-loaded in the CLI Tool terminal by running the command:

```
==> using token <token value>
```

Note that there is an expiration date on the token so if the above command does not work, just re-generate a new token.

## 3.2. API Interaction Examples

The subsections which follow document interaction with some of the EBSI APIs provided by the demonstrator. All interactions are done within the pilot platform (set in the EBSI CLI tool using command `env pilot`). This section simply provides a snapshot of commands/interactions feasible with EBSI API. See the [CLI Tool documentation](https://ec.europa.eu/digital-building-blocks/code/projects/EBSI/repos/test-scripts/browse#cli-commands) for the full set of possible commands and interactions.

### 3.2.1. DID Registry API
The [DID Registry API](https://api.preprod.ebsi.eu/docs/apis/did-registry/latest#/) is used to list and verify valid DIDs which have been anchored on the EBSI platform. 

The endpoint is: https://api.preprod.ebsi.eu/did-registry/v3/

Example Usage:
```
did get /identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC #valid DID
did get /identifiers/did:ebsi:z123GCLrLYbkubAjuqQZAAA #invalid DID
```

Above commands are equivalent of making the follow HTTP GET requests in a browser:

https://api.preprod.ebsi.eu/did-registry/v3/identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC

https://api.preprod.ebsi.eu/did-registry/v3/identifiers/did:ebsi:z123GCLrLYbkubAjuqQZAAA


### 3.2.2. Timestamp API

The [timestamp API](https://api.preprod.ebsi.eu/docs/apis/timestamp/latest#/) is used for generating/linking/verifying timestamps for record keeping purposes. 

The endpoint is: https://api.preprod.ebsi.eu/timestamp/v3/

Example Usage:

```
==> timestamp timestampHashes #generates a new timestamp
==> view transactionInfo #Views the transaction result
Timestamp hashes
{
  "data": {
    "test": "1b542f44f18e99f48266a69f"
  },
  "id": "uEiBhsNLvNKmC6sxQTRVz00vgggGIcofiKlYWgfwUXk5H7A"
}
```

The above generated timestamp can be viewed live here: 

https://api.preprod.ebsi.eu/timestamp/v3/timestamps/uEiBhsNLvNKmC6sxQTRVz00vgggGIcofiKlYWgfwUXk5H7A

### 3.2.3. Proxy Data Hub API 
The [Proxy Data Hub API](https://api.preprod.ebsi.eu/docs/apis/proxy-data-hub/latest#/) is designed to allow for off-chain storage of owner data which may be considered private or sensitive. It implements end-to-end encryption using a traditional cassandra database in order to comply with GDPR.

The endpoint is: https://api.preprod.ebsi.eu/proxy-data-hub/v3/

Example Usage:

```
datahub insert {"value":"private data"} private #example of inserting private data attribute
datahub insert {"value":"shared data"} shared #example of inserting shared data attribute
datahub get /attributes/<hash> #get attribute data based on hash
datahub get /attributes #list all attributes which have been uploaded to EBSI 
```

# 4. Sign and Verify Message using EBSI DID  (Python Code)
The scripts contained in this repository provides example of how the DID public key, anchored on the EBSI platform, can be used to verify a signed message. To execute the Python code, run the following commands:

```
pip install -r requirements.txt
python verify.py
```

The script `verify.py` is used to verify a message which was signed with user [did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC](https://api.preprod.ebsi.eu/did-registry/v2/identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC)'s public key. The script `sign.py` provides example of signing a message (update the private key parameter and corresponding public key with your own value to sign/verify another message).
