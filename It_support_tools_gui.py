import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import psutil
import shutil
import subprocess
import hashlib
from datetime import datetime
import platform
from ttkthemes import ThemedTk

class ITSupportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛠️ IT Support Tool Suite")
        self.root.geometry("900x700")
        
        # Set custom colors
        self.colors = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'button_bg': '#3498DB',
            'button_hover': '#2980B9',
            'output_bg': '#34495E',
            'output_fg': '#E0E0E0'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Create style for widgets
        style = ttk.Style()
        style.configure('Custom.TFrame', background=self.colors['bg'])
        style.configure('Custom.TButton', 
                       padding=10, 
                       font=('Helvetica', 10, 'bold'),
                       background=self.colors['button_bg'])
        style.configure('Title.TLabel', 
                       font=('Helvetica', 16, 'bold'), 
                       foreground=self.colors['fg'],
                       background=self.colors['bg'])
        
        # Create main frame
        main_frame = ttk.Frame(root, style='Custom.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add title
        title_label = ttk.Label(main_frame, 
                               text="🚀 IT Support Tool Suite", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create output text area with custom colors
        self.output_text = tk.Text(main_frame, 
                                 height=20, 
                                 width=80, 
                                 bg=self.colors['output_bg'],
                                 fg=self.colors['output_fg'],
                                 font=('Consolas', 11),
                                 padx=10,
                                 pady=10)
        self.output_text.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create scrollbar with custom colors
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.output_text.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.output_text['yscrollcommand'] = scrollbar.set
        
        # Create buttons frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Button configurations with emojis
        buttons = [
            ("💾 Check Disk Space", self.check_disk_dialog),
            ("📊 Monitor Bandwidth", self.monitor_bandwidth),
            ("📝 List Processes", self.list_processes),
            ("⏰ Create Task", self.create_task_dialog),
            ("🖥️ System Inventory", self.collect_inventory),
            ("📁 Rotate Logs", self.rotate_logs_dialog),
            ("🔍 Find Duplicates", self.find_duplicates_dialog),
            ("👥 User Sessions", self.track_user_sessions)
        ]
        
        # Create animated buttons with hover effect
        for idx, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, 
                          text=text,
                          command=command,
                          bg=self.colors['button_bg'],
                          fg=self.colors['fg'],
                          font=('Helvetica', 10, 'bold'),
                          relief='raised',
                          borderwidth=2,
                          width=20,
                          height=2)
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)
            
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(b))
            btn.bind('<Leave>', lambda e, b=btn: self.on_leave(b))

    def on_hover(self, button):
        button.configure(bg=self.colors['button_hover'])

    def on_leave(self, button):
        button.configure(bg=self.colors['button_bg'])

    def write_output(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"✨ {text}")

    def check_disk_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Check Disk Space")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Drive:").grid(row=0, column=0, padx=5, pady=5)
        drive_entry = ttk.Entry(dialog)
        drive_entry.insert(0, "C:/")
        drive_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Threshold (%):").grid(row=1, column=0, padx=5, pady=5)
        threshold_entry = ttk.Entry(dialog)
        threshold_entry.insert(0, "20")
        threshold_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def check():
            drive = drive_entry.get()
            threshold = int(threshold_entry.get())
            total, used, free = shutil.disk_usage(drive)
            free_percentage = (free / total) * 100
            result = f"Drive: {drive}\nFree Space: {free_percentage:.2f}%\n"
            if free_percentage < threshold:
                result += f"Warning: Free space on {drive} is below {threshold}%!"
            else:
                result += f"Disk space is sufficient on {drive}."
            self.write_output(result)
            dialog.destroy()
        
        ttk.Button(dialog, text="Check", command=check).grid(row=2, column=0, columnspan=2, pady=10)

    def monitor_bandwidth(self):
        counters = psutil.net_io_counters()
        result = f"Bytes Sent: {counters.bytes_sent / (1024 ** 2):.2f} MB\n"
        result += f"Bytes Received: {counters.bytes_recv / (1024 ** 2):.2f} MB"
        self.write_output(result)

    def list_processes(self):
        result = ""
        for proc in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
            result += f"PID: {proc.info['pid']}, Name: {proc.info['name']}, "
            result += f"Memory: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB\n"
        self.write_output(result)

    def create_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Scheduled Task")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Script Path:").grid(row=1, column=0, padx=5, pady=5)
        path_entry = ttk.Entry(dialog)
        path_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        time_entry = ttk.Entry(dialog)
        time_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def create():
            try:
                command = f"schtasks /create /tn {name_entry.get()} /tr {path_entry.get()} /sc once /st {time_entry.get()}"
                subprocess.run(command, shell=True, check=True)
                self.write_output(f"Scheduled task '{name_entry.get()}' created.")
            except Exception as e:
                self.write_output(f"Failed to create scheduled task: {e}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Create", command=create).grid(row=3, column=0, columnspan=2, pady=10)

    def collect_inventory(self):
        result = "System Information:\n"
        result += f"OS: {platform.system()} {platform.release()}\n"
        result += f"Processor: {platform.processor()}\n"
        result += f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        result += f"Disk Space: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB"
        self.write_output(result)

    def rotate_logs_dialog(self):
        log_dir = filedialog.askdirectory(title="Select Log Directory")
        if log_dir:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = f"{log_dir}/archive_{timestamp}"
                shutil.make_archive(archive_path, 'zip', log_dir)
                
                for file in os.listdir(log_dir):
                    if file.endswith(".log"):
                        os.remove(os.path.join(log_dir, file))
                
                self.write_output(f"Logs archived to {archive_path}.zip\nOld logs deleted.")
            except Exception as e:
                self.write_output(f"Error rotating logs: {e}")

    def find_duplicates_dialog(self):
        directory = filedialog.askdirectory(title="Select Directory to Check for Duplicates")
        if directory:
            result = ""
            seen = {}
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = self.hash_file(file_path)
                    if file_hash in seen:
                        result += f"Duplicate found:\n{file_path}\nand\n{seen[file_hash]}\n\n"
                    else:
                        seen[file_hash] = file_path
            self.write_output(result if result else "No duplicates found.")

    def hash_file(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def track_user_sessions(self):
        result = ""
        sessions = psutil.users()
        for session in sessions:
            result += f"User: {session.name}\nTerminal: {session.terminal}\n"
            result += f"Started: {datetime.fromtimestamp(session.started)}\n\n"
        self.write_output(result)

def main():
    root = ThemedTk(theme="equilux")  # Using themed Tk for better looking widgets
    app = ITSupportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
