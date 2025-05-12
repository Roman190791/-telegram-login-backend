from fastapi import FastAPI, Request
import hashlib
import hmac
from fastapi.responses import HTMLResponse

app = FastAPI()

BOT_TOKEN = "7933363751:AAHKXlfZv-FLyihdQiKTMTp6nVS-B0yelKA"  # Заміни на реальний токен від BotFather

def check_telegram_auth(data: dict) -> bool:
    auth_data = data.copy()
    hash_to_check = auth_data.pop("hash", "")
    
    data_check_string = "\n".join(f"{k}={auth_data[k]}" for k in sorted(auth_data))
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(calculated_hash, hash_to_check)

@app.get("/auth/telegram")
async def auth_telegram(request: Request):
    query_params = dict(request.query_params)
    if check_telegram_auth(query_params):
        user = query_params.get("username", "невідомий")
        return HTMLResponse(f"<h1>Привіт, {user}! Авторизація успішна.</h1>")
    else:
        return HTMLResponse("<h1>Помилка: авторизація не пройдена.</h1>", status_code=403)
