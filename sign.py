#Sources:
#   https://jwcrypto.readthedocs.io/en/latest/jwk.html
#   https://jwcrypto.readthedocs.io/en/latest/jws.html

from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

#This is the private key values for user did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC as anchored on EBSI. 
#See https://api.preprod.ebsi.eu/did-registry/v2/identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC
#The actual private key value d has been intentionally removed. Replace with your own values.
ebsi_private_key = {
        "kty": "EC",
        "crv": "secp256k1",
        "y": "JvytX9oOAozeyRXHhdzaw1E8I5QFfGIW73SZsHH628Y",
        "x": "AHkB24a8GqpUqZPG9wkP9FNJsSKbwzSkZPAoPF6EFrI",
        "d": "<private key value>" 
      }

private_key = jwk.JWK(**ebsi_private_key)

payload = "This is an example of a signed message using my private key"
jwstoken = jws.JWS(payload.encode('utf-8'))

jwstoken.add_signature(private_key, None, json_encode({"alg": "ES256K"}), json_encode({"kid": private_key.thumbprint()}))

print(jwstoken.serialize()) #print out the signed message. Copy the contents over to verify.py to verify.