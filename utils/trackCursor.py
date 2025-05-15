import os
from pprint import pprint

import yaml

def StoreCursor(has_next_page: bool, next_cursor: str, new_tweet_count: int, tweet_ids: list):
    # Specify the file path
    cursor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'cursor.yml')
    cursor_path = os.path.abspath(cursor_path)

    try:
        print("[StoreCursor][Info] Reading cursor.yml ...")
        with open(cursor_path, 'r') as file:
            cursor_data = yaml.safe_load(file) or {'pages': {}}

            # Find highest page number and set new page number
            current_pages = [int(page) for page in cursor_data['pages'].keys()]
            new_page_number = max(current_pages, default=0) + 1

            # Prepare data to store
            page_data = {
                "has_next_page": has_next_page,
                "next_page": next_cursor,
                "tweets_per_page": new_tweet_count,
                "ids": f'[{", ".join(str(id) for id in tweet_ids)}]'
            }

        try:
            print("[StoreCursor][Info] Storing latest cursor to cursor.yml ...")
            if str(new_page_number) in cursor_data['pages']:
                print(f"[StoreCursor][Error] Page '{new_page_number}' already in file. Next page @[...{next_cursor[-10:]}]")
            else:
                # Add entry to (existing) data
                cursor_data['pages'][str(new_page_number)] = page_data
                print("[StoreCursor][Success] Adding following cursor data to file:")
                # pprint(cursor_data)

                with open(cursor_path, "w", encoding='utf-8') as f:
                    yaml.dump(cursor_data, f, allow_unicode=True, sort_keys=True)
                    print("[StoreCursor][Success] Updated cursor.yml file. Continuing ...")

        except Exception as e:
            print("[StoreCursor][Error] Failed to store latest cursor to cursor.yml")
            print(e)
            raise

    except Exception as e:
        print("[StoreCursor][Error] Failed to read cursor.yml")
        print(e)
        raise


def ReadCursor():
    cursor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'twitter', 'cursor.yml')
    cursor_path = os.path.abspath(cursor_path)

    try:
        print("[ReadCursor][Info] Reading current cursor from cursor.yml ...")
        with open(cursor_path, 'r') as file:
            cursor_data = yaml.safe_load(file) or {'pages': {}}

            # Prüfe ob 'pages' existiert und Daten enthält
            if not cursor_data.get('pages'):
                print("[ReadCursor][Info] Keine Seiten gefunden, starte von Anfang")
                return ''

            try:
                # Finde die höchste Seitennummer
                last_page = str(max(int(page) for page in cursor_data['pages'].keys()))

                # Sicherer Zugriff auf die Daten
                page_data = cursor_data['pages'].get(last_page, {})
                cursor = page_data.get('next_page', '')

                if cursor:
                    print(f"[ReadCursor][Info] Found cursor [...{cursor[-10:]}]")
                else:
                    print("[ReadCursor][Info] Kein cursor gefunden, starte von Anfang")

                return cursor

            except ValueError as e:
                print("[ReadCursor][Warning] Keine gültigen Seitennummern gefunden")
                return ''

    except FileNotFoundError as e:
        print(f"[ReadCursor][Error] {str(e)}")
        raise
    except Exception as e:
        print(f"[ReadCursor][Error] Unerwarteter Fehler: {str(e)}")
        raise





