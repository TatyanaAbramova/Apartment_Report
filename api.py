from model import Model
import uvicorn
from fastapi import FastAPI

app = FastAPI()
model = Model()


@app.post('/predict/')
def predict_price(flat_info: dict):
    return model.predict(flat_info)


def main() -> None:
    """Run application"""
    uvicorn.run("api:app", host="localhost")


if __name__ == '__main__':
    main()
