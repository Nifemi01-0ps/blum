from utils.core import create_sessions
from utils.telegram import Accounts
from utils.blum import Blum
from data.config import hello, USE_PROXY
import asyncio
import os

async def main():
    print(hello)
    action = int(input("Select action:\n1. Create sessions\n2. Start claimer\n\n> "))

    if not os.path.exists('sessions'):
        os.mkdir('sessions')

    if action == 1:
        await create_sessions()

    if action == 2:
        accounts = await Accounts().get_accounts()
        with open('proxy.txt', 'r') as file:
            proxy = [i.strip() for i in file.readlines()]
        tasks = []
        if USE_PROXY:
             
            proxy_dict = {}
 
            with open('proxy.txt','r') as file:
 
                proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
 
                for prox,name in proxy:
 
                    proxy_dict[name] = prox

            for thread, account in enumerate(accounts):

                if account in proxy_dict:

                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy_dict[account]).main()))
                else:
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
