from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def getinfo():
    return({'messages' : "getting the information from user"})

