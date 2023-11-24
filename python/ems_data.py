import jwt
import os  # required only for reading env variables


PRIVATE_KEY: str = os.environ['EMS_PRIVATE_KEY']
COMPANY_NAME: str = os.environ['EMS_COMPANY']


def get_token(company_name):
    # f = open('private_key.pem', 'r')
    # key = f.read()
    key = PRIVATE_KEY
    headers = {'alg': 'RS512', 'typ': 'JWT', 'kid': company_name}
    encoded = jwt.encode({'identity': ''}, key=key, algorithm='RS512',
                         headers=headers)
    encoded = 'Bearer ' + encoded
    # f.close()
    return encoded
