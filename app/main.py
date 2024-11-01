#main.py

import os
import aiofiles
import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, HTTPException   
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

drop_path = "drop"
dl_path = "share"

app = FastAPI()

print (f"{os.getcwd()}/static")
app.mount("/static", StaticFiles(directory=f"{os.getcwd()}/static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/download")
async def download(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})

@app.post("/files/upload")
async def upload(request: Request, files: list[UploadFile] = File(...)):
        for file in files:
            async with aiofiles.open(drop_path + "/" + file.filename, "wb") as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)

        return templates.TemplateResponse("success.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

