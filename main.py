import sys
import os
import webbrowser
from openai_wrapper import Client
from screenshot import save_screenshot, get_clipboard, file_dialog
from display import generate_html

MENU_WIDTH = 64

def main():
    print('Initializing OpenAI client...')
    client = Client() # initialize OpenAI client
    response = None

    # load default prompt
    if os.path.isfile('default_prompt.txt'):
        with open('default_prompt.txt', 'r') as f:
            client.sys_prompt = f.read()

    # parse command line arguments
    open_in_browser = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            print(f'''Usage: {os.path.basename(sys.argv[0])} [options]
Options:
    -h, --help                                 Show this help message and exit
    -t, --max-completion-tokens <NUM_TOKENS>   Set max_completion_tokens (default: 1000)
    -p, --system-prompt <PATH_TO_PROMPT>       Set system prompt from file
    -b, --open-in-browser                      Open responses in browser
    -m, --model <MODEL>                        Set model (default: gpt-4o)'''
            )
            return
        elif sys.argv[i] == '-p' or sys.argv[i] == '--system-prompt':
            if os.path.isfile(fpath := sys.argv[i + 1]):
                with open(fpath, 'r') as f:
                    client.sys_prompt = f.read()
            else:
                print(f'File not found {fpath}')
                return
        elif sys.argv[i] == '-t' or sys.argv[i] == '--max-completion-tokens':
            client.max_completion_tokens = int(sys.argv[i + 1])
        elif sys.argv[i] == '-b' or sys.argv[i] == '--open-in-browser':
            open_in_browser = True
        elif sys.argv[i] == '-m' or sys.argv[i] == '--model':
            client.model = sys.argv[i + 1]

    os.system('cls' if os.name == 'nt' else 'clear')

    # main menu loop
    while True:
        choice = input(f'''{'Menu'.center(MENU_WIDTH, '-')}
    1) Take a screenshot          5) Set max_completion_tokens
    2) Choose image file          6) Send prompt from clipboard
    3) Set system prompt          7) Set model
    4) Open response in browser   0) Exit

Select an option (0-7): '''
        )
        print()

        match choice:
            case '0': # Exit
                return
            
            case '1': # Take a screenshot
                try:
                    save_screenshot('out.png')
                except ValueError:
                    print('Screenshot failed')
                    continue
                
                response = client.create_completion(image_path='out.png')

            case '2': # Choose image file
                if os.path.isfile(fpath := file_dialog([('Image files', '*.png;*.jpg;*.jpeg;*.webp;*.gif')])):
                    print(f'File chosen: {fpath}')
                    response = client.create_completion(image_path=fpath)
                else:
                    print(f'File not found {fpath}')
                    continue

            case '3': # Set system prompt
                print(f'Current system prompt: {client.sys_prompt}\n')
                choice = input('1) Load from file\n2) Enter new system prompt\nSelect an option or press Enter to go back: ')
                if choice == '1':
                    if os.path.isfile(fpath := file_dialog([('Text files', '*.txt')])):
                        with open(fpath, 'r') as f:
                            client.sys_prompt = f.read()
                    else:
                        print(f'File not found {fpath}')
                elif choice == '2':
                    client.sys_prompt = input('Enter new system prompt: ')
                    if client.sys_prompt == '':
                        client.sys_prompt = None
                    print(f'System prompt set to: {client.sys_prompt}')

                continue

            case '4': # Open response in browser
                if response is None:
                    print('No response to open')
                    continue

            case '5': # Set max_completion_tokens
                print(f'Current max_completion_tokens: {client.max_completion_tokens}')
                while True:
                    try:
                        max_completion_tokens = input(f'Enter new max_completion_tokens or press Enter to go back: ')
                        if max_completion_tokens == '':
                            break
                        else:
                            client.max_completion_tokens = int(max_completion_tokens)
                            print(f'max_completion_tokens set to: {client.max_completion_tokens}')
                            break
                    except ValueError:
                        print('Invalid input')
                
                continue

            case '6': # Send prompt from clipboard
                try:
                    prompt = get_clipboard()
                except ValueError:
                    print('Clipboard is empty')
                    continue

                print(f'Prompt from clipboard: {prompt}')
                response = client.create_completion(txt_prompt=prompt)
            
            case '7': # Set model
                print(f'Current model: {client.model}')
                model = input(f'Enter new model or press Enter to go back: ')
                if model == '':
                    continue
                else:
                    client.model = model
                    print(f'Model set to: {client.model}')
                    continue

            case _:
                print('Invalid input')
                continue

        
        print(f'{f'Response from {client.model}'.center(MENU_WIDTH, '-')}\n{response}')

        if open_in_browser or choice == '4':
            with open('response.html', 'w') as f:
                f.write(generate_html(response))

            webbrowser.open('response.html')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass