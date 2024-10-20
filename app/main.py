import uvicorn
from fastapi import FastAPI
from app.routers import category, products, auth

app = FastAPI()

@app.get("/")
async def welcome():
    return {'message': "My e-commerce app"}

app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)