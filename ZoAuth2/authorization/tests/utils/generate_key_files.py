from authlib.jose import ECKey

def create_key_pair():
    keys = ECKey.generate_key(is_private=True)
    private_key_file = open('private_key.json', 'w')
    private_key_file.write(keys.as_json())
    private_key_file.close()

    public_key_file = open('public_key.pem', 'wb')
    public_key_file.write(keys.as_pem(is_private=False))
    public_key_file.close()

create_key_pair()
