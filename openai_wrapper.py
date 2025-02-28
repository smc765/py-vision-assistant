from dotenv import load_dotenv
import os
import base64
import logging
import requests

DEFAULT_MAX_COMPLETION_TOKENS = 1000
DEFAULT_MODEL = 'gpt-4o'
API_URL = 'https://api.openai.com/v1'

# logging configuration
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING) # log only warnings and errors to console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('openai.log', mode='w'), # log to file
                        console_handler
                    ])

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class Client:
    def __init__(self, max_completion_tokens=DEFAULT_MAX_COMPLETION_TOKENS, model=DEFAULT_MODEL, api_url = API_URL):
        self.max_completion_tokens = max_completion_tokens
        self.model = model
        self.sys_prompt = None
        self.api_url = api_url

        load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))) # load environment variables from .env
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key is None:
            raise ValueError('OPENAI_API_KEY environment variable not set')

    def create_completion(self, txt_prompt=None, image_path=None):
        messages=[]
        
        if self.sys_prompt is not None:
            messages.append({'role': 'developer', 'content': self.sys_prompt})

        if txt_prompt is not None:
            messages.append({'role': 'user', 'content': txt_prompt})
        
        if image_path is not None:
            messages.append({'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{encode_image(image_path)}'}}]})

        if len(messages) == 0:
            raise ValueError('No prompt provided')

        logger.info(f'REQUEST model={self.model}, messages={messages}, max_completion_tokens={self.max_completion_tokens}') # log request
        print('waiting for response...')

        endpoint = f'{self.api_url}/chat/completions'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_completion_tokens": self.max_completion_tokens
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload).json()
        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {e}')
            return

        logger.info(f'RESPONSE {response}') # log response

        if (response['choices'])[0]['finish_reason'] != 'stop':
            logger.warning(f'Response not finished. finish_reason: {(response['choices'])[0]['finish_reason']}')

        return ((((response['choices'])[0])['message'])['content'])

def main():
    client = Client(max_completion_tokens=100)
    print(client.create_completion(txt_prompt='This is a test prompt. Respond with Hello World'))

if __name__ == '__main__':
    main()