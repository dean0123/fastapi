from fastapi import FastAPI, Depends, Response,Request
from fastapi import Form
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.responses import HTMLResponse,RedirectResponse
#from typing import Annotated

from ad     import verify_user_pass
from ad_jwt import encode_jwt, decode_jwt

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
app=FastAPI()

@app.get('/ap01')                           # 模擬 RP ：一般 AP 網頁 或 API
async def ap01(req :Request ):
    token=req.cookies.get('access_token')
    return HTMLResponse(f"<H2> A Simple AP Auth Page or Function </h2>")

@app.get('/')                               
@app.get('/me')                              # 模擬 IDP ID Provider，Auth Server
def me(req :Request, client_id:str='me', cb_url:str='/me' ):      # 呼叫方 傳入call back URL
    token=req.cookies.get('access_token')    # 從Cookie取JWT Token
    if token:                                # 有Token
        payload=decode_jwt(token.replace("Bearer ",""))   # 把Token 前面的 Bearer 去掉
        if payload.get('Error') :            # 有Token 但過期/驗證失敗/有Error，就重新轉到 Login 畫面
            return login(client_id,cb_url)   # =======> 重新登入認證
        else:
            return {'access_token': token, 'token_type': 'bearer'}  #登入完成 傳回 JWT Token 給 RP
    else: return login(client_id,cb_url)     # Cookie沒JWT Token ->沒登入過/已登出  =======> 重新登入認證

    #HTML="<H2> 登入完成，可以用了 </h2>"
    #HTML="<H2> 傳回 JWT Token </h2>"
    #HTML+=f'<pre>{token}<p>{payload}</pre>'
    #return HTMLResponse(HTML) 
    return {'access_token': token, 'token_type': 'bearer'}  #登入完成 傳回 JWT Token 給 RP


@app.post('/auth')
def auth( req: Request, resp:  Response, 
                client_id: str=Form(), 
                cb_url:    str=Form(), 
                form_data: OAuth2PasswordRequestForm = Depends()):
    user_ad_attr = verify_user_pass(form_data.username,form_data.password)

    if not user_ad_attr:            # 沒傳回 AD Attr 都當作登入失敗
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登入失敗，帳號密碼有誤 Incorrect username or password!",
        )
    jwt=encode_jwt(user_ad_attr)    # 登入成功後，把User AD Attr編入JWT Token寫入Cookie
    #rr=RedirectResponse(url=f'cb_url?jwt={jwt}', status_code=status.HTTP_303_SEE_OTHER)
    rr=RedirectResponse(url=f'{cb_url}?jwt={jwt}', status_code=status.HTTP_303_SEE_OTHER)
    rr.set_cookie(key='access_token',value=f'Bearer {jwt}', httponly=True)  # jwt 存 Cookie httponly 
    return rr

@app.get("/logout")
async def logout(resp: Response):
    resp.delete_cookie(key="access_token")
    return {"message": "Cookie 'access_token' cleared"}
    

@app.get("/login" )
def login( client_id:str='default', cb_url:str='/'):
    print( '--------> Login : client_id = ',client_id)
    print( '--------> Login : cb_url = ',cb_url)
#def login():
    return HTMLResponse(f"""
    
    <form method='post' action='/auth'>
        <input               name='username' placeholder='Username' />
        <input               name='password' type='password' placeholder='Password' />
        <input type='hidden' name='client_id' value='{client_id}' placeholder='client_id' />
        <input type='hidden' name='cb_url' value='{cb_url}' placeholder='cb_url' />
        <input type='hidden' name='client_secret' value='' placeholder='secret'  />
        <input type='hidden' name='state' value='456' />
        <button type='submit'>Login</button>
        <br> client id = {client_id}
        <br> call back URL = {cb_url}
    </form>
    """)
