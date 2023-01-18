from telethon.sync import TelegramClient
from os.path import exists
import json
import os

def check_login():
    if exists('config.json'):
        with open('config.json', 'r') as f:
            cfg = json.load(f)
        phone = cfg['number']
        session_name = f'{phone}.session'
        apid = cfg['api_id']
        ihash = cfg['api_hash']
        return session_name, apid, ihash 
    else:
        return new_login()


def new_login():
    phone = str(input('input number (example: +77719999999): '))
    session_name = f'{phone}.session'
    apid = str(input('input api_id: '))
    ihash = str(input('input api_hash: '))
    info = {'number':phone, "api_id":apid, "api_hash":ihash}
    with open('config.json', 'w') as f:
        json.dump(info, f, indent = 4)
    return session_name, apid, ihash


def get_dialog(client):
    dialogs = client.get_dialogs()
    channels = []
    for dialog in dialogs:
        if dialog.is_channel:
            channels.append(dialog)
    for index,channel in enumerate(channels):
        name_channel = channel.title
        t = f'[{index}] {name_channel}'
        print(t)
    num_group = int(input('input what you need: '))
    return channels[num_group]


def check_dirs(info_c):
    if not exists(f'{info_c}_photos'):
        os.mkdir(f'./{info_c}_photos')
    if not exists(f'{info_c}_documents'):
        os.mkdir(f'./{info_c}_documents')


def save_text(text_list:list, info_c):
    text = text_list[::-1]
    with open(f'./{info_c}_text.txt', 'w') as f:
        f.write('\n'.join(text))


def main():
    session, apid, ihash = check_login()
    client = TelegramClient(session, apid, ihash)
    client.start()
    print('connected successfully')
    dialog = get_dialog(client)
    info_c = f"{dialog.name}(ID_{dialog.id})"
    check_dirs(info_c)
    text_list = []

    index = 0
    while True:
        for_work = 0
        messages = client.iter_messages(dialog.id, min_id = index, max_id= index+11)
        client.get
        for message in messages:
            for_work = 1
            date = message.date.strftime("%Y-%m-%d %H:%M")
            if not message.sender_id:
                send_id = 'empty'
            else:
                send_id = message.sender_id
            if message.photo:
                print(f'Download photo id_msg = {message.id}, please wait...')
                message.download_media(f'./{info_c}_photos//')
            if message.document:
                size = int(message.document.size)/1024/1024
                size = round(size, 2)
                print(f'Download document id_msg = {message.id} size = {size}MB, please wait...')
                message.download_media(f'./{info_c}_documents//')
            if message.text:
                text = f"[{date}] {send_id}: {message.text}"
                text_list.append(text)
        index += 10
        if for_work == 0:
            save_text(text_list, info_c)
            break
    client.disconnect()


if __name__ == '__main__':
    main()