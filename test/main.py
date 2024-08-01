import tkinter as tk
from frames import create_frames

def main():
    root = tk.Tk()
    root.title("Balance Personal")
    root.minsize(1100,356)
    create_frames(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()