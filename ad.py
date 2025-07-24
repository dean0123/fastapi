# -------  ldap 3 is faster and better then regular ldap library ----------
from ldap3 import Server, Connection, SUBTREE

AD_SERVER = Server( '10.1.220.1')            # AD Server IP, 可用 nslookup 找
BASE_NAME = "dc=compeq,dc=com,dc=tw"         # LDAP Bind/Search Base Name, 一般就是 Domain DC
ATTRIBUTE = ['sAMAccountName','mail','department','cn']  # 要找的AD Attr屬性，sAMAccountName就是帳號

def verify_user_pass(user: str, pwd:str):
    c=Connection(AD_SERVER, user=f'{user}@compeq.com.tw', password=pwd)
    if c.bind():                         # Bind AD/LDAP成功，就是帳號密碼驗證ok/登入ok
        return get_user_info(c, user)    # Bind AD/LDAP成功後，抓 User 相關data 回傳
    else:
        return                           # 不能bind 表示登入失敗：回覆null [] 空值，讓接收端處理:帳號密碼不正確
        
def get_user_info(c: Connection, user: str):
    c.search( BASE_NAME, f'(&(objectclass=user)(sAMAccountName={user}))', SUBTREE, attributes=ATTRIBUTE)
    if c.entries: 
        import json
        entry_json=json.loads(c.entries[0].entry_to_json()) 
        return entry_json                # 只抓第一筆，轉seriablizable JSON 格式回傳
        return c.entries[0].entry_raw_attributes.entry_to_json()       # 只抓第一筆，轉seriablizable JSON 格式回傳
    else: 
        return                                     # 沒找到User 就回覆null [] 空值，讓接收端處理:帳號密碼不正確 

