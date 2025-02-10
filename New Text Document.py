import psutil
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw
import pystray

def update_stats():
    """Update CPU and RAM usage in real-time."""
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    cpu_label.config(text=f"CPU: {cpu_usage}%")
    ram_label.config(text=f"RAM: {ram_usage}%")
    root.after(1000, update_stats)  # Update every second

def toggle_visibility():
    """Minimize or restore the window."""
    root.withdraw()
    create_tray_icon()

def create_tray_icon():
    """Create a system tray icon to restore or close the window."""
    def restore():
        root.deiconify()
        icon.stop()
    
    def close():
        icon.stop()
        root.destroy()
    
    # Create an image for the tray icon
    image = Image.new('RGB', (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(100, 100, 100))
    
    # Create tray icon
    icon = pystray.Icon("SysMonitor", image, menu=pystray.Menu(
        pystray.MenuItem("Restore", lambda _: restore()),
        pystray.MenuItem("Close", lambda _: close())
    ))
    icon.run()

def start_move(event):
    """Start moving the window."""
    root.x = event.x
    root.y = event.y

def stop_move(event):
    """Stop moving the window."""
    root.x = None
    root.y = None

def on_motion(event):
    """Move the window based on cursor movement."""
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"200x80+{x}+{y}")

# Main window setup
root = tk.Tk()
root.title("System Monitor")
root.geometry("200x80")
root.configure(bg="#333")
root.overrideredirect(True)  # Removes title bar
root.attributes("-topmost", True)  # Keep on top

# Enable window dragging
root.bind("<ButtonPress-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", on_motion)

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#333", foreground="white")

# CPU and RAM labels
cpu_label = ttk.Label(root, text="CPU: 0%", style="TLabel")
cpu_label.pack(pady=5)
ram_label = ttk.Label(root, text="RAM: 0%", style="TLabel")
ram_label.pack()

# Minimize button
toggle_button = tk.Button(root, text="⏬", command=toggle_visibility, bg="#444", fg="white", bd=0)
toggle_button.pack(side=tk.BOTTOM, fill=tk.X)

# Start updating stats
update_stats()

# Show window
root.mainloop()
