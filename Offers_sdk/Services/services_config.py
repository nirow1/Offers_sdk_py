import aiohttp


base_aiohttp_config = {
    "headers": {
        "Accept": "application/json",
    },
    "timeout": aiohttp.ClientTimeout(total=30),
}