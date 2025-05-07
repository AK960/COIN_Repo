import os
from configparser import ConfigParser, Error as ConfigError
from typing import Optional

def ReadApiKey() -> Optional[str]:
    """
        Liest den API-Key aus der config.ini Datei.

        Returns:
            str: Der API-Key wenn erfolgreich gelesen

        Raises:
            FileNotFoundError: Wenn die config.ini Datei nicht gefunden wurde
            ConfigError: Wenn die Konfigurationsdatei nicht korrekt gelesen werden konnte
            KeyError: Wenn der API-Key in der Konfigurationsdatei fehlt
            ValueError: Wenn der API-Key leer oder ungültig ist
        """

    api_key: str | None = None

    try:
        print("[ReadApiKey][Info] Reading api-key from config.ini ...")
        config = ConfigParser()

        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'conf', 'config.ini')
        config_path = os.path.abspath(config_path)

        if not config.read(config_path):
            raise FileNotFoundError("Config file not found.")

        if 'TWITTERAPI' not in config:
            raise KeyError("Section 'TWITTERAPI' not found in config file.")

        api_key = config['TWITTERAPI']['API_KEY']

        if not api_key:
            raise ValueError("API Key not found in config file.")

        print(f"[ReadApiKey][Info] API Key gefunden: [{api_key[:5]}...]")
        return api_key

    except FileNotFoundError as e:
        print(f"[ReadApiKey][Error] Failed to find config file.")
        print(e)
        raise

    except ConfigError as e:
        print("[ReadApiKey][Error] Failed reading config.ini")
        print(e)
        raise

    except KeyError as e:
        print(f"[ReadApiKey][Error] Failed reading key.")
        print(e)
        raise

    except Exception as e:
        print(f"[ReadApiKey][Error] Unexpected failure.")
        print(e)
        raise