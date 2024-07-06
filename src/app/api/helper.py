from ..schemas.base_account import BaseAccountRead
import urllib.parse
import hashlib
import hmac
# def check_permission(acc: BaseAccountRead, permission: int) -> bool:
#     return acc['permission'] == permission

def convert_interest_by_interest_each_month(interest: int, interest_type: int):
    if interest_type == 2:
        return interest / 3
    elif interest_type == 3:
        return interest / 12
    else:
        return interest

def get_payment_url(vnpay_payment_url, secret_key, requestData):
    # Sort the request data by keys
    inputData = sorted(requestData.items())
    
    queryString = ''
    seq = 0
    
    # Construct the query string from sorted data
    for key, val in inputData:
        if seq == 1:
            queryString += "&" + key + '=' + urllib.parse.quote_plus(str(val))
        else:
            seq = 1
            queryString = key + '=' + urllib.parse.quote_plus(str(val))

    # Generate HMAC SHA-512 hash of the query string with the secret key
    hashValue = hmac.new(secret_key.encode('utf-8'), queryString.encode('utf-8'), hashlib.sha512).hexdigest()
    
    # Construct the final payment URL with the query string and secure hash
    return vnpay_payment_url + "?" + queryString + '&vnp_SecureHash=' + hashValue


class Vnpay:
    def __init__(self):
        self.responseData = {}

    def validate_response(self, secret_key):
        vnp_SecureHash = self.responseData.get('vnp_SecureHash', '')

        # Remove hash params
        self.responseData.pop('vnp_SecureHash', None)
        self.responseData.pop('vnp_SecureHashType', None)

        # Sort and hash the remaining parameters
        inputData = sorted(self.responseData.items())
        hasData = ''
        seq = 0
        for key, val in inputData:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData = hasData + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                else:
                    seq = 1
                    hasData = str(key) + '=' + urllib.parse.quote_plus(str(val))

        hashValue = self.__hmacsha512(secret_key, hasData)

        # print('Validate debug, HashData:', hasData)
        # print('HashValue:', hashValue)
        # print('InputHash:', vnp_SecureHash)

        return vnp_SecureHash == hashValue

    def __hmacsha512(self, key, data):
        byteKey = key.encode('utf-8')
        byteData = data.encode('utf-8')
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

