#Sources:
#   https://jwcrypto.readthedocs.io/en/latest/jwk.html
#   https://jwcrypto.readthedocs.io/en/latest/jws.html

from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

#This is the public key values for user did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC as anchored on EBSI. 
#See https://api.preprod.ebsi.eu/did-registry/v2/identifiers/did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC
ebsi_public_key = {
"y":"JvytX9oOAozeyRXHhdzaw1E8I5QFfGIW73SZsHH628Y",
"x":"AHkB24a8GqpUqZPG9wkP9FNJsSKbwzSkZPAoPF6EFrI",
"crv":"secp256k1",
"kty":"EC"}

public_key = jwk.JWK(**ebsi_public_key)

#Signature to verify is defined below.
#Note that the payload value contains signed message in base64 format
#The payload, decoded, reads: "This is an example of a signed message using my private key"
#Changing the payload or other values will result in failed verification
#as the message would no longer be the same as the one signed with user 
#did:ebsi:zZ8fawYd3YGXZ3mzJhY1CJC's corresponding private key.
sig = '{"header":{"kid":"sXBAElAzc8qAKpyvlNc77pTXyKOvaZql0ZgIPRjSz8M"},"payload":"VGhpcyBpcyBhbiBleGFtcGxlIG9mIGEgc2lnbmVkIG1lc3NhZ2UgdXNpbmcgbXkgcHJpdmF0ZSBrZXk","protected":"eyJhbGciOiJFUzI1NksifQ","signature":"SKbDYoJWCZBWDb9ntD6iUtVQ2qlMvbWnqgfVU-WNSWCI7uehu7xYiDINqJazHFMVvNNNsQVSwincXi8GYX2RXg"}'
jwstoken = jws.JWS()
jwstoken.deserialize(sig)
jwstoken.verify(public_key)
payload = jwstoken.payload


#Print out the signed message in plaintext if valid. Otherwise, an exeption is raised if payload is altered.
print("Verification passed! Payload verified:\n {0}".format(payload))