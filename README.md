# PyVision Assistant

PyVision Assistant is a customizable AI screenshot tool that uses the OpenAI API to intelligently parse and process information from captured images.

## Setup

    pip install -r requirements.txt

## Usage

    python main.py [options]  
        Options:  
            -h, --help                                 Show this help message and exit  
            -t, --max-completion-tokens <NUM_TOKENS>   Set max_completion_tokens (default: 1000)  
            -p, --system-prompt <PATH_TO_PROMPT>       Set system prompt from file  
            -b, --open-in-browser                      Open responses in browser  
            -m, --model <MODEL>                        Set model (default: gpt-4o)  

## Using Custom Prompts

System prompts are plain-text instructions that are sent to the AI model alongside the user's prompt. They're used to define the behavior of the AI Assistant, enabling customization for a wide range of use cases. There are a few ways to set a custom system prompt. By default, the prompt is loaded from `default-prompt.txt` located in the program's directory. Alternatively, the path to a prompt file can be specified using the `--system-prompt <PATH>` argument.

## Building a Standalone Executable

PyVision Assistant can be compiled into a portable executable with the following steps:  

### 1. Install [PyInstaller](https://pyinstaller.org/en/stable/)

### 2. Configure Enviornment Variables

- Create a text file named `.env` and add the line: `OPENAI_API_KEY=<YOUR_API_KEY>`  

### 3. Compile the program with the included [build.bat](https://github.com/smc765/py-vision-assistant/blob/main/build.bat) script or with the command  

    pyinstaller --onefile --console --add-data=".env:." main.py

- The executable will be saved to: `/dist/main.exe`
