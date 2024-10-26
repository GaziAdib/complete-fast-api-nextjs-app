from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.products import router as product_router
from app.db_config.prisma_config import connect_prisma, disconnect_prisma
from contextlib import asynccontextmanager
# for statsic files

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Adding Middleware for nextjs 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount for static files
# app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_prisma()
        yield
    finally:
        await disconnect_prisma()

app = FastAPI(lifespan=lifespan)


app.include_router(product_router, prefix='/api')


# Entry point for Uvicorn to serve the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




 






# import asyncio
# from fastapi import FastAPI
# from app.api.products import router as product_router
# from prisma import Prisma

# app = FastAPI()

# async def main() -> None:
#     prisma = Prisma()
#     await prisma.connect()

#     # Write your queries here

#     app.include_router(product_router, prefix="/api")

# if __name__ == "__main__":
#     asyncio.run(main())