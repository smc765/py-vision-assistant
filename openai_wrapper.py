from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import logging
from logging.handlers import RotatingFileHandler

DEFAULT_MAX_COMPLETION_TOKENS = 1000
DEFAULT_MODEL = 'gpt-4o'

# logging configuration
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING) # log only warnings and errors to console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        RotatingFileHandler('openai.log', maxBytes=1000000, backupCount=1), # log to file with rotation
                        console_handler
                    ])

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class Client:
    def __init__(self, max_completion_tokens=DEFAULT_MAX_COMPLETION_TOKENS, model=DEFAULT_MODEL):
        self.max_completion_tokens = max_completion_tokens
        self.model = model
        self.sys_prompt = None

        load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))) # load environment variables from .env
        self.client = OpenAI()

    def create_completion(self, txt_prompt=None, image_path=None, messages=[]):
        if self.sys_prompt is not None:
            messages.append({'role': 'developer', 'content': self.sys_prompt})

        if txt_prompt is not None:
            messages.append({'role': 'user', 'content': txt_prompt})
        
        if image_path is not None:
            messages.append({'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{encode_image(image_path)}'}}]})

        if len(messages) == 0:
            raise ValueError('No prompt provided')

        logger.info(f'Completion: model={self.model}, messages={messages}, max_completion_tokens={self.max_completion_tokens}')
        print('waiting for response...')

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=self.max_completion_tokens
            )
        except Exception as e:
            logger.error(e)
            return None

        if response.choices[0].finish_reason == 'length':
            logger.warning('The completion was truncated to the maximum token length')

        logger.info(f'Response: {response}')
        return response.choices[0].message.content
    
def main():
    client = Client(max_completion_tokens=100)
    print(client.create_completion(txt_prompt='What is the capital of France?'))

if __name__ == '__main__':
    main()