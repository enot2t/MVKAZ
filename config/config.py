from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,  # "DYNACONF",
    environments=True,  # Автоматически использовать секцию текущей среды
    settings_files=['settings.toml', '.env.toml'],
    env_switcher="ENV_FOR_DYNACONF",
    load_dotenv=True
)