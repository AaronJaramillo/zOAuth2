from bitcoinrpc.authproxy import AuthServiceProxy
import requests
from authlib.jose import ECKey
from auth import ecdsaJWT
from authlib.integrations.requests_client import OAuth2Session
import time

node = AuthServiceProxy('http://user:password@0.0.0.0:38232')

def node_setup():
    address = node.getnewaddress()#'tmQj7xUdizNE8uNqiDBkVUBtNrydkQtjpn4'
    #node.generate(500)
    print(node.sendtoaddress(address, 100))
    node.generate(10)
    print(address)
    return address

FROM_ADDRESS = node_setup()



def get_products():
    response = requests.get('http://127.0.0.1:8000/api/get_products')
    return response.json()

def pay_for_product(_fromAddress, _address, _amount, _memo):
    print(_address)
    print(_amount)
    print(_memo)
    return node.z_sendmany(_fromAddress, [{
        'address': _address,
        'amount': _amount,
        'memo': _memo,
    }])

def create_key_pair():
    keys = ECKey.generate_key(is_private=True)
    public_key = keys.as_pem(is_private=False)
    private_key = keys.as_pem(is_private=True)

    public_file = open('public.pem', 'wb')
    public_file.write(public_key)
    public_file.close()

    private_file = open('private.pem', 'wb')
    private_file.write(private_key)
    private_file.close()

    # return public_key as pem
    return public_key

    #jose.generate_key
    #save as pem file
    #convert public key to hex bytes
    #return hex
def key_to_hex(key):
    return key.hex()

def load_private_key_from_file():
    pem_file = open('private.pem', 'rb')
    private_key_pem = pem_file.read()
    pem_file.close()

    return ECKey.import_key(private_key_pem)

def get_pubkey_thumbprint(keys):
    ##takes in a private key, needs to make thumbprint from public key
    ##this seems like kind of a round about way of doing this.
    public = ECKey.import_key(keys.as_pem(is_private=False))
    return public.thumbprint()

#def create_session
    # make oauth2session
    # authenticat
    # make endpoint request
def get_first_product_and_purchase():
    fromAddress = FROM_ADDRESS
    products = get_products()
    public_key = create_key_pair()
    print(public_key.hex())
    return pay_for_product(fromAddress, products[0]['address'], products[0]['price']/(10**8), public_key.hex())

def authorize_session():
    keys = load_private_key_from_file()
    client_id = get_pubkey_thumbprint(keys)
    print(client_id)
    print(keys)
    token_endpoint = 'http://127.0.0.1:8000/api/token'
    session = OAuth2Session(
        client_id,
        keys,
        token_endpoint_auth_method='ecdsa_key_jwt',
        scope='premium'
    )
    session.register_client_auth_method(ecdsaJWT(token_endpoint))
    print(session.fetch_token(token_endpoint, grant_type='client_credentials'))
    print(session.request('get', 'http://127.0.0.1:8000/api/premium').json())

def main():
    print(get_first_product_and_purchase())
    node.generate(5)
    time.sleep(10)
    requests.get('http://127.0.0.1:8000/backend/scan_transactions')
    time.sleep(10)
    authorize_session()

main()
