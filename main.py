from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import models
from database import engine
from routes import ws_router, country_router, city_router, street_router

# Create DataBase
models.Base.metadata.create_all(bind=engine)

# Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="WebApiFinalProject",
    summary="Chat with WebSockets & Notifications of CRUD operations",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})


app.include_router(ws_router)
app.include_router(country_router)
app.include_router(city_router)
app.include_router(street_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
