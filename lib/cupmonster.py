import asyncio

from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import FuncaptchaProxylessRequest

client_options = ClientOptions(api_key='801b4c09a5347eeae0cb3a460df08769')
cap_monster_client = CapMonsterClient(options=client_options)


async def solve_captcha():
    return await cap_monster_client.solve_captcha(recaptcha2request)


recaptcha2request = FuncaptchaProxylessRequest(websiteUrl="https://tinder.com/",
                                               websitePublicKey="B5B07C8C-F93F-44A8-A353-4A47B8AD5238")

responses = asyncio.run(solve_captcha())
print(responses)
