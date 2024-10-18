from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.products import router as product_router
from app.db_config.prisma_config import connect_prisma, disconnect_prisma
# for statsic files

from fastapi.staticfiles import StaticFiles

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
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.on_event("startup")
async def startup():
    await connect_prisma()  # Connect Prisma at startup

@app.on_event("shutdown")
async def shutdown():
    await disconnect_prisma()  # Disconnect Prisma at shutdown

app.include_router(product_router, prefix="/api")

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