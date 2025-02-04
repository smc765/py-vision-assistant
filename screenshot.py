import tkinter as tk
from PIL import ImageGrab
import ctypes

class Screenshot:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg='black')
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.rect = None
        self.screenshot = None

        self.canvas = tk.Canvas(root, cursor="cross", bg="grey11")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Key>", lambda x: self.root.destroy()) # exit when any key is pressed

        self.label = tk.Label(
            self.canvas,
            text=' Select reigon to screenshot or press any key to exit... ',
            font=("Arial", 16), 
        )
        self.label.pack(pady=10)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        try:
            x1 = min(self.start_x, self.current_x)
            y1 = min(self.start_y, self.current_y)
            x2 = max(self.start_x, self.current_x)
            y2 = max(self.start_y, self.current_y)
        except Exception:
            print('Invalid selection')
            return
        
        self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.root.destroy()

def save_screenshot(filename='out.png'):
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 ) # Minimize window
    root = tk.Tk()
    app = Screenshot(root)
    root.mainloop()
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 9 ) # Restore window
    if app.screenshot is None:
        raise ValueError("Screenshot failed")
    app.screenshot.save(filename)
    print(f'Screenshot saved as: {filename}')

def main():
    save_screenshot()

if __name__ == '__main__':
    main()