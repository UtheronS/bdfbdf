from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
import asyncio

async def fetch_nft_holders(rpc_url, collection_address):
    """
    Получает всех владельцев NFT коллекции через RPC-соединение.
    """
    async with AsyncClient(rpc_url) as client:
        # Запрашиваем все токен-аккаунты, связанные с коллекцией
        response = await client.get_program_accounts(
            Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),  # SPL Token Program
            encoding="jsonParsed",
            filters=[
                {"dataSize": 165},  # Размер данных для токен-аккаунта
                {"memcmp": {"offset": 32, "bytes": collection_address}}  # Фильтр по адресу коллекции
            ]
        )

        if response.get("result"):
            accounts = response["result"]
            holders = []
            for account in accounts:
                account_data = account["account"]["data"]["parsed"]["info"]
                owner = account_data["owner"]
                balance = int(account_data["tokenAmount"]["amount"])
                if balance > 0:  # Если баланс токенов больше 0
                    holders.append(owner)
            return list(set(holders))  # Убираем дубликаты
        else:
            print("Не удалось получить данные о холдерах.")
            return []

def save_holders_to_file(holders, filename="nft_holders.txt"):
    """
    Сохраняет список адресов в текстовый файл.
    """
    with open(filename, "w") as file:
        for holder in holders:
            file.write(f"{holder}\n")
    print(f"Адреса успешно сохранены в файл {filename}")

async def main():
    # RPC-сервер Solana (можно использовать публичный)
    rpc_url = "https://api.mainnet-beta.solana.com"

    # Адрес коллекции (Metaplex Collection Address)
    collection_address = "ваш_адрес_коллекции"

    print(f"Получение владельцев для коллекции: {collection_address}")
    holders = await fetch_nft_holders(rpc_url, collection_address)
    
    if holders:
        print(f"Найдено {len(holders)} владельцев.")
        save_holders_to_file(holders)
    else:
        print("Не удалось найти владельцев.")

if __name__ == "__main__":
    asyncio.run(main())
