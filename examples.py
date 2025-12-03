import asyncio

from uuid import UUID
from dotenv import load_dotenv
from Offers_sdk.offers_api_client import OffersApiClient
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest

async def example():
    # Construct a product request (could come from user input, DB, etc.)
    product = RegisterProductRequest(
        id=UUID("559e878-1425c-41d4-a987-4800854206976"),
        name="Real Product",
        description="This is a real product"
    )
    product_list = [RegisterProductRequest(
        id=UUID("560e898-1425c-41d4-a987-476855440500"),
        name="Real Product",
        description="This is a real product"
        ),
        RegisterProductRequest(
            id=UUID("570e898-1425c-41d4-a987-476855440500"),
            name="Real Product",
            description="This is a real product"
        ),
        RegisterProductRequest(
            id=UUID("580e898-1425c-41d4-a987-476855440500"),
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

        offers = await client.get_offers("559e878-1425c-41d4-a987-4800854206976")
        print("Offers:", offers)

if __name__ == "__main__":
    asyncio.run(example())