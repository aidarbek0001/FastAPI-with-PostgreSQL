from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str = 'd6458bde4a7b86d490174e8b29ef5ca587dd16b0cbe5df93b8c634b298937f3c'
