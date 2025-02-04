import sys
import os
import webbrowser
import tkinter as tk
from tkinter import filedialog
from openai_wrapper import Client
from screenshot import save_screenshot

MENU_WIDTH = 36

# returns path of file chosen or empty string if no file was chosen
def file_dialog(filetypes=[('All files', '*.*')]):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    fpath = filedialog.askopenfilename(filetypes=filetypes)
    root.destroy()
    return fpath

def main():
    client = Client() # initialize OpenAI client
    response = None

    if os.path.isfile('default_prompt.txt'):
        with open('default_prompt.txt', 'r') as f:
            client.sys_prompt = f.read()

    # parse command line arguments
    open_in_browser = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            print(f'''Usage: {os.path.basename(sys.argv[0])} [options]
Options:
    -h, --help                    Show this help message and exit
    -t, --max-completion-tokens   Set max_completion_tokens
    -p, --system-prompt           Set system prompt
    -b, --open-in-browser         Open response in browser
    -m, --model                   Set model (default: gpt-4o)'''
            )
            return
        elif sys.argv[i] == '-p' or sys.argv[i] == '--system-prompt':
            if os.path.isfile(fpath := sys.argv[i + 1]):
                with open(fpath, 'r') as f:
                    client.sys_prompt = f.read()
        elif sys.argv[i] == '-t' or sys.argv[i] == '--max-completion-tokens':
            client.max_completion_tokens = int(sys.argv[i + 1])
        elif sys.argv[i] == '-b' or sys.argv[i] == '--open-in-browser':
            open_in_browser = True
        elif sys.argv[i] == '-m' or sys.argv[i] == '--model':
            client.model = sys.argv[i + 1]

    while True:
        choice = input(f'''{'Menu'.center(MENU_WIDTH, '-')}
    1) Take a screenshot
    2) Choose image file
    3) Set system prompt
    4) Open response in browser
    5) Set max_completion_tokens (current: {client.max_completion_tokens})
    6) Send prompt from clipboard
    7) Set model (current: {client.model})
    0) Exit

Select an option (0-7): '''
        )

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
                    print(f'File not found')
                    continue

            case '3': # Set system prompt
                print(f'Current system prompt: {client.sys_prompt}')
                choice = input('1) Load from file\n2) Enter new system prompt\nSelect an option (1-2): ')
                if choice == '1':
                    if os.path.isfile(fpath := file_dialog([('Text files', '*.txt')])):
                        with open(fpath, 'r') as f:
                            client.sys_prompt = f.read()
                    else:
                        print(f'File not found')
                        continue
                elif choice == '2':
                    client.sys_prompt = input('Enter new system prompt: ')
                    
                print(f'System prompt set to: {client.sys_prompt}')
                continue

            case '4': # Open response in browser
                if response is None:
                    print('No response to open')
                    continue

            case '5': # Set max_completion_tokens
                while True:
                    try:
                        client.max_completion_tokens = int(input('Enter new max_completion_tokens: '))
                        break
                    except ValueError:
                        print('Invalid input')
                
                print(f'max_completion_tokens set to: {client.max_completion_tokens}')
                continue

            case '6': # Send prompt from clipboard
                root = tk.Tk()
                root.withdraw()
                try:
                    prompt = root.clipboard_get()
                except tk.TclError:
                    print('Clipboard is empty')
                    continue
                finally:
                    root.destroy()

                print(f'Prompt from clipboard: {prompt}')
                response = client.create_completion(txt_prompt=prompt)
            
            case '7': # Set model
                client.model = input('Enter new model (ex. gpt-4o): ')
                print(f'Model set to: {client.model}')

        if response is not None:
            print(f'{f'Response from {client.model}'.center(MENU_WIDTH, '-')}\n{response}')

            if open_in_browser or choice == '4':
                with open('response.html', 'w') as f:
                    f.write(f'<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n{response}')
                webbrowser.open('response.html')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass