from typing import List
from app.schemas.product_schema import ProductCreate, ProductUpdate, Product as ProductSchema
from app.db_config.prisma_config import prisma


class ProductService:
    async def get_all_products(self) -> List[ProductSchema]:
        prisma_products = await prisma.product.find_many()
        return [ProductSchema(**product.dict()) for product in prisma_products]

    async def get_product_by_id(self, id: str) -> ProductSchema:
        product = await prisma.product.find_unique(where={'id': id})
        if not product:
            return None
        return ProductSchema(**product.dict())

    async def create_product(self, product: ProductCreate) -> ProductSchema:
        new_product = await prisma.product.create(data=product.dict())
        return ProductSchema(**new_product.dict())

    async def update_product(self, id: str, product: ProductUpdate) -> ProductSchema:
        updated_product = await prisma.product.update(
            where={'id': id},
            data=product.dict(exclude_unset=True)
        )
        return ProductSchema(**updated_product.dict())

    async def delete_product_by_id(self, id: str) -> ProductSchema:
        deleted_product = await prisma.product.delete(where={'id': id})
        return ProductSchema(**deleted_product.dict())

    async def get_products_by_query(self, query: str) -> List[ProductSchema]:
        query_products = await prisma.product.find_many(where={'category': {'contains': query}})
        return [ProductSchema(**product.dict()) for product in query_products]












# from typing import List
# from app.schemas.product_schema import ProductCreate, ProductUpdate, Product as ProductSchema
# from app.db_config.prisma_config import prisma


# class ProductService:
#     async def get_all_products(self) -> List[ProductSchema]:
#         prisma_products = await prisma.product.find_many()
#         return [ProductSchema(**product.dict()) for product in prisma_products]

#     async def get_product_by_id(self, id: str) -> ProductSchema:
#         product = await prisma.product.find_unique(where={'id': id})
#         if not product:
#             return None
#         return ProductSchema(**product.dict())

#     async def create_product(self, product: ProductCreate) -> ProductSchema:
#         new_product = await prisma.product.create(data=product.dict())
#         print(new_product)
#         return ProductSchema(**new_product.dict())

#     async def update_product(self, id: str, product: ProductUpdate) -> ProductSchema:
#         updated_product = await prisma.product.update(
#             where={'id': id},
#             data=product.dict(exclude_unset=True)
#         )
#         return ProductSchema(**updated_product.dict())

#     async def delete_product_by_id(self, id: str) -> ProductSchema:
#         deleted_product = await prisma.product.delete(where={'id': id})
#         return ProductSchema(**deleted_product.dict())





# from prisma import Prisma
# from typing import List
# from app.schemas.product_schema import ProductCreate, ProductUpdate, Product as ProductSchema

# class ProductService:
#     def __init__(self):
#         self.prisma = Prisma()

#     async def connect(self):
#         # Ensure the Prisma client is connected
#         if not self.prisma.is_connected():
#             await self.prisma.connect()    

#     async def get_all_products(self) -> List[ProductSchema]:
#         await self.connect()  # Ensure the Prisma client is connected
#         prisma_products = await self.prisma.product.find_many()

#         #Convert Prisma products to Pydantic products
#         return [ProductSchema(**product.dict()) for product in prisma_products]

#     async def get_product_by_id(self, id: str) -> ProductSchema:
#         await self.connect()
#         product = await self.prisma.product.find_unique(where={'id': id})

#         if not product:
#             return None
#         return ProductSchema(**product.dict())

#     async def create_product(self, product: ProductCreate) -> ProductSchema:
#         await self.connect()
#         new_product = await self.prisma.product.create(data=product.dict())

#         return ProductSchema(**new_product.dict())

#     async def update_product(self, id: str, product: ProductUpdate) -> ProductSchema:
#         await self.connect()
#         updated_product = await self.prisma.product.update(
#             where={'id': id},
#             data=product.dict(exclude_unset=True)
#         )
#         return ProductSchema(**updated_product.dict())

#     async def delete_product_by_id(self, id: str) -> ProductSchema:
#         await self.connect()
#         deleted_product = await self.prisma.product.delete(where={'id': id})

#         return ProductSchema(**deleted_product.dict())

#     async def disconnect(self):
#         await self.prisma.disconnect()  # Disconnect the Prisma client when done