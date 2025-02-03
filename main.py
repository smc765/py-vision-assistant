import sys
import os
import webbrowser
import tkinter as tk
from tkinter import filedialog
from openai_wrapper import OpenaiWrapper
from screenshot import save_screenshot

MENU_WIDTH = 36

def main():
    client = OpenaiWrapper()
    response = None

    # parse command line arguments
    open_in_browser = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p' or sys.argv[i] == '--system-prompt':
            client.sys_prompt = sys.argv[i + 1]
        elif sys.argv[i] == '-m' or sys.argv[i] == '--max-completion-tokens':
            client.max_completion_tokens = int(sys.argv[i + 1])
        elif sys.argv[i] == '-b' or sys.argv[i] == '--open-in-browser':
            open_in_browser = True

    while True:
        try:
            choice = input(f'''{'Menu'.center(MENU_WIDTH, '-')}
    1) Take a screenshot
    2) Choose image file
    3) Set system prompt
    4) Open response in browser
    5) Set max_completion_tokens
    6) Send prompt from clipboard
    0) Exit

Select an option (0-6): '''
        )
        except KeyboardInterrupt:
            return

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
                root = tk.Tk()
                root.attributes("-topmost", True)
                fpath = filedialog.askopenfilename()
                root.destroy()
                if os.path.isfile(fpath):
                    print(f'File selected: {fpath}')
                    response = client.create_completion(image_path=fpath)
                else:
                    print(f'File not found')
                    continue

            case '3': # Set system prompt
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

        if response is not None:
            print(f'{f'Response from {client.model}'.center(MENU_WIDTH, '-')}\n{response}')

            if open_in_browser or choice == '4':
                with open('response.html', 'w') as f:
                    f.write(f'<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n{response}')
                webbrowser.open('response.html')

if __name__ == '__main__':
    main()