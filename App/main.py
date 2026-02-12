from fastapi import FastAPI

app = FastAPI()

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}