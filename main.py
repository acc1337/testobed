from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, EditBannedRequest
from telethon.tl.types import ChannelParticipantsSearch, ChatBannedRights
import asyncio

# Введите свои учетные данные
api_id = '21559674'
api_hash = '1c2a41ffcd266172a0fc340eab42652b'
channel_username = 'obed4688'  # Юзернейм или ID вашего канала

# Права на блокировку (чтобы фактически "удалить" пользователей, можно заблокировать их)
ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True  # Этот флаг запрещает доступ к сообщениям (блокировка)
)

# Создаем клиента
client = TelegramClient('session_name', api_id, api_hash)

async def remove_all_members():
    await client.start()
    
    # Получаем канал
    channel = await client.get_entity(channel_username)
    
    # Получаем участников канала
    participants = await client(GetParticipantsRequest(
        channel=channel,
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=100,  # Максимум 100 участников за раз, можно повторить запросы
        hash=0
    ))

    # Перебираем участников и блокируем их
    for user in participants.users:
        try:
            await client(EditBannedRequest(channel, user.id, ban_rights))
            print(f'User {user.id} has been removed')
            await asyncio.sleep(1)  # Добавляем задержку, чтобы избежать лимитов
        except Exception as e:
            print(f'Failed to remove user {user.id}: {e}')

    print("All users processed.")

# Запускаем удаление участников
with client:
    client.loop.run_until_complete(remove_all_members())