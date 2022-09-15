
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.config import load_config_cli, load_config
from chia.util.ints import uint32, uint16
from chia.util.bech32m import decode_puzzle_hash
from chia.wallet.util.wallet_types import WalletType
from chia.wallet.puzzle_drivers import PuzzleInfo
from typing import Union, Dict

import disnake

async def sendgold(user, amount, address, message):

    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    wallet_rpc_port = config['wallet']['rpc_port']
    wallet_client = await WalletRpcClient.create('localhost', uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config)
    wallets = await wallet_client.get_wallets()
    embed = disnake.Embed(
        title=f"Gold not sent",
        description=f"Gold could not be sent at this moment.",
        color=0xE02B2B
    )
    try:
        for wallet in wallets:
            print(wallet)
            if wallet["name"] == "Gold":
                if amount < 101:
                    result = await wallet_client.cat_spend(wallet_id=wallet["id"], amount=amount*1000, inner_address=address)
                    print(f"Sent {amount} gold to {user.display_name} ({user.name})")
                    embed = disnake.Embed(
                        title=f"{user.display_name} earned {amount} gold!",
                        description=message,
                        color=disnake.Color.gold()
                    )

                else:
                    print(f"Did not send gold to {user.name}")
                    embed = disnake.Embed(
                        title=f"Gold not sent",
                        description=f"You tried to send too much.",
                        color=0xE02B2B
                    )
    except Exception as e:
        print(e)
        embed = disnake.Embed(
            title=f"Gold not sent",
            description=f"Gold could not be sent at this moment.",
            color=0xE02B2B
        )
    wallet_client.close()
    return embed

async def offertest():

    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    wallet_rpc_port = config['wallet']['rpc_port']
    wallet_client = await WalletRpcClient.create('localhost', uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config)

    nfts = await wallet_client.list_nfts(3)

    f = open("offercommands.bat", 'w')

    for nft in nfts['nft_list']:
        goblinNum = nft['chain_info'].split(".jpg")[0].split("/")[-1]
        f.write(f"echo y|chia wallet make_offer -r 2:100 -o {nft['launcher_id'].split('0x')[1]}:1 -p ./GoblinData/offers/GrinningGoblin#{goblinNum}-100gold.offer -f 1949239784\n")









    wallet_client.close()
