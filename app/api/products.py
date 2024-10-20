from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.product_schema import Product, ProductCreate, ProductUpdate
from app.services.product_service import ProductService
import logging
import os
from fastapi import UploadFile, File, Form
import shutil


router = APIRouter()

#for image upload
product_service = ProductService()


# Create a logger instance
logger = logging.getLogger(__name__)

@router.get("/products/", response_model=List[Product], status_code=status.HTTP_200_OK)
async def get_products(product_service: ProductService = Depends()):
    products = await product_service.get_all_products()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products



@router.put("/product/{id}/update", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(id: str, product: ProductUpdate, product_service: ProductService = Depends()):
    existing_product = await product_service.get_product_by_id(id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    updated_product = await product_service.update_product(id, product)
    logger.info(f"Product with id {id} updated successfully.")
    return updated_product

@router.delete("/product/{id}/delete", response_model=Product, status_code=status.HTTP_200_OK)
async def delete_product(id: str, product_service: ProductService = Depends()):
    product = await product_service.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Use the exact image path stored in the DB
    image_path = product.image  # e.g., 'static/images/imagename'

    # Ensure the path is based on the root directory
    root_dir = os.getcwd()
    full_image_path = os.path.join(root_dir, image_path)
    print('full_image_path', full_image_path)

    if os.path.exists(full_image_path):
        os.remove(full_image_path)
        logger.info(f"Image {full_image_path} deleted successfully.")
    else:
        logger.warning(f"Image {full_image_path} not found.")

    deleted_product = await product_service.delete_product_by_id(id)
    logger.info(f"Product with id {id} deleted successfully.")
    
    return deleted_product


@router.get("/products/{id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_single_product(id:str, product_service: ProductService = Depends()):
    product = await product_service.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product found")
    return product


@router.post('/product/create', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    title: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None),  # Optional image file
    product_service: ProductService = Depends()
):
    
    image_url = None

    if image:

        image_directory = "static/images"
        os.makedirs(image_directory, exist_ok=True)

        image_path = f"static/images/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = image_path

     # Create a ProductCreate object from the form data
    product_data = ProductCreate(
        title=title,
        price=price,
        description=description,
        category=category,
        image=image_url
    )

    #use the product service to create the product
    created_product = await product_service.create_product(product_data)
    logger.info(f"Product '{title}' created successfully.")

    return created_product          

# async def create_product(product: ProductCreate, product_service: ProductService = Depends()):
#     created_product = await product_service.create_product(product)
#     logger.info(f"Product '{product.title}' created successfully.")
#     return created_product


@router.get("/products", response_model=List[Product], status_code=status.HTTP_200_OK)
async def get_products_by_query(query:str, product_service: ProductService = Depends()):
    products = await product_service.get_products_by_query(query)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products
