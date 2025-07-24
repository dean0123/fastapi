#from jose import jwt 
#from datetime import datetime, timedelta
                                   # export LANG=zh_TW.utf-8 to user Chinese 
import jwt                         # JWT 包含 (1)HEADER  (2)Payload (3)Signature
import datetime                    
import time

ALGORITHM  = "HS256"               # alg 演算法包含在 jwt HEADER  { 'alg':'HS256', 'typ':'JWT' } 
SECRET_KEY = "secret-key 123 abc"  # key 會用 HEADER Payload -> 產生 Signature 來驗證整個 JWT
                                   # 定義 jwt 的 payload
payload = {                                  
    "sub": 123, 
    "ad_attr": "",                 # A place holder 佔位 用來裝 AD Attr 
    "exp": ""                      # Token expires in 24 hours
    # 其他還有 sub(ject),iss(uer),aud(ience) 等public payload，沒一定要用
}

def encode_jwt(ad_attr: str ):
    payload['ad_attr']=ad_attr     # 先把傳入JSON 的AD Attr屬性整包放入Payload，再包進jwt token (暫時做法)
    payload['exp']= datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=600) # Token expires in 24 hours
    print("\n\n------ ad_jwt.py encode token attr ------\n\n",payload['ad_attr']['attributes'])
    print("\n\n------ ad_jwt.py encode token attr ------\n\n",payload['ad_attr']['attributes'])
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str  ):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("\n\n------ ad_jwt.py decode_jwt token attr ------\n\n",payload['ad_attr']['attributes'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'Error':'JWT Token Signature Expired'}

    except jwt.InvalidTokenError:
        return {'Error':'JWT Token is Invalid'}

