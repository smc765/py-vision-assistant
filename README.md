# PyVision Assistant

PyVision Assistant is a customizable AI screenshot tool that enables intelligent text extraction and anaylisis of images through the use of user-defined prompts 

## Setup
    pip install -r requirements.txt

## Usage:
    python main.py [options]  
        Options:  
            -h, --help                                 Show this help message and exit  
            -t, --max-completion-tokens <NUM_TOKENS>   Set max_completion_tokens (default: 1000)  
            -p, --system-prompt <PATH_TO_PROMPT>       Set system prompt from file  
            -b, --open-in-browser                      Open responses in browser  
            -m, --model <MODEL>                        Set model (default: gpt-4o)  
  
## Building a Standalone Executable
#### Step 1: Install [PyInstaller](https://pyinstaller.org/en/stable/)
#### Step 3: Configure Enviornment Variables
- Create a text file named `.env` and add the line: `OPENAI_API_KEY=<YOUR_API_KEY>`
    
#### Step 2: Compile the program with the included [build.bat](https://github.com/smc765/py-vision-assistant/blob/main/build.bat) script or with the command:
    pyinstaller --onefile --console --add-data=".env:." main.py
- The executeable will be saved as: `/dist/main.exe`
