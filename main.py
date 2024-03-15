from fastapi import FastAPI
from user.user import user
from product.product import product

app = FastAPI()

app.mount("/v2", product)
app.mount("/v1", user)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
