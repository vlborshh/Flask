from fastapi import FastAPI

from uvicorn import run
from sem5.app.app1.app1 import app1
from sem5.app.app2.app2 import app2
from sem5.app.app3.app3 import app3
from sem5.app.app6.app6 import app6
from sem5.app.app7.app7 import app7
from sem5.app.app8.app8 import app8

app = FastAPI()

app.mount('/sem5/app/app2', app2)
app.mount('/sem5/app/app3', app3)
app.mount('/sem5/app/app1', app1)
app.mount('/sem5/app/app6', app6)
app.mount('/sem5/app/app7', app7)
app.mount('/sem5/app/app8', app8)

@app.get('/')
async def root():
    return {'message': 'Hello world'}



if __name__ == '__main__':
    run("main:app", host='127.0.0.1', port=8000, reload=True)

