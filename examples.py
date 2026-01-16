import asyncio

from uuid import UUID
from dotenv import load_dotenv
from src.Offers_sdk.offers_api_client import OffersApiClient
from src.Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest

async def example():
    # Construct a product request (could come from user input, DB, etc.)
    # todo validation at product creation level
    product = RegisterProductRequest(
        id=UUID("550e9400-e29b-41d4-a716-446685444000"),
        name="Real Product",
        description="This is a real product"
    )
    product_list = [RegisterProductRequest(
        id=UUID("6fa459ea-ee8a-4ca4-894e-db77e160355e"),
        name="Real Product",
        description="This is a real product"
        ),
        RegisterProductRequest(
            id=UUID("123e4567-e89b-42d3-a456-556642440000"),
            name="Real Product",
            description="This is a real product"
        ),
        RegisterProductRequest(
            id=UUID("9a7b330a-a736-4f05-bfef-3f0f379b6d19"),
            name="Real Product",
            description="This is a real product"
        )
                    ]

    load_dotenv()

    # Use the client as a context manager
    async with OffersApiClient() as client:
        result = await client.register_product(product)
        print("Product registered successfully:", result)

        result = await client.batch_register_products(product_list)
        print("Batch product registration results:", result)

        offers = await client.get_offers(str(product.id))
        print("Offers:", offers)

if __name__ == "__main__":
    asyncio.run(example())