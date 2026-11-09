from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "task_manager"
    DB_USER: str = "postgres"
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()

# файл config.py нужен для централизованного хранения, загрузки и проверки настроек приложения.
#
# В нашем Task Manager API он хранит настройки PostgreSQL (адрес, порт, имя БД, логин, пароль), загружает их из .env и предоставляет остальным модулям через объект settings.
#
# Главная цель: не прописывать настройки подключения и секреты вручную в каждом файле проекта.