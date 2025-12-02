import asyncio

from uuid import UUID
from dotenv import load_dotenv
from Offers_sdk.offers_api_client import OffersApiClient
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest

async def main():
    # Construct a product request (could come from user input, DB, etc.)
    product = RegisterProductRequest(
        id=UUID("550e890-1429c-41d4-a787-446655440000"),
        name="Real Product",
        description="This is a real product"
    )

    load_dotenv()

    # Use the client as a context manager
    async with OffersApiClient() as client:
        try:
            #result = await client.register_product(product)
            #print("Product registered successfully:", result)

            offers = await client.get_offers("550e840-1429c-41d4-a788-486655440000")
            print("Offers:", offers)

        except ValueError as e:
            print("Validation failed:", e)
        except RuntimeError as e:
            print("Runtime error:", e)

if __name__ == "__main__":
    asyncio.run(main())