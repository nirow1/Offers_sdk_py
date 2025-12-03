Offers SDK

welcome to my take on the offers SDK

Instructions:
1. Download the SDK from the official repository, unzip and place the 'offers_sdk' folder in your project directory.
2. Create and define your .env file in the root of your project with the following variables:
   - REFRESH_TOKEN
   - MAX_API_REQUEST_RETRIES
   - API_BASE_URL
   example provided in file .env.example
3. Install the required dependencies listed in requirements.txt using pip:
   pip install -r requirements.txt or any other method you prefer.
4. Import the OffersApiClient class from Offers_sdk_py.Offers_sdk module in your Python script:
   from Offers_sdk_py.Offers_sdk.offers_api_client import OffersApiClient
5. From there you can use class OffersApiClient to interact with the Offers API, using it as context manager:
   with OffersApiClient() as client:
       ...

examples of usage are provided in the examples.py file.