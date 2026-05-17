from dotenv import load_dotenv
import os

_ = load_dotenv()

LLM_Config: dict[str, str] = {
    "BASE_URL": f'{os.getenv("BASE_URL", "")}',
    "API_KEY": f'{os.getenv("API_KEY", "")}',
    "Model": f'{os.getenv("MODEL", "")}',
}
