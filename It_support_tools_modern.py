import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import psutil
import shutil
import subprocess
import hashlib
from datetime import datetime
import platform

class ModernITSupportGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("IT Support Tool Suite")
        self.root.geometry("1000x800")
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.main_frame, 
            text="IT Support Tool Suite",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Create output text area
        self.output_text = ctk.CTkTextbox(
            self.main_frame,
            height=400,
            font=ctk.CTkFont(size=12)
        )
        self.output_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create scrollable button frame
        self.button_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            height=200
        )
        self.button_frame.pack(fill="x", padx=20, pady=20)
        
        # Create modern button grid
        self.create_buttons()

    def create_buttons(self):
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
        
        for i, (text, command) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            btn = ctk.CTkButton(
                self.button_frame,
                text=text,
                command=command,
                width=200,
                height=40,
                font=ctk.CTkFont(size=13),
                corner_radius=8
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

    def write_output(self, text):
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", f"✨ {text}")

    def check_disk_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Check Disk Space")
        dialog.geometry("400x250")
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Drive:").pack(pady=5)
        drive_entry = ctk.CTkEntry(frame)
        drive_entry.insert(0, "C:/")
        drive_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Threshold (%):").pack(pady=5)
        threshold_entry = ctk.CTkEntry(frame)
        threshold_entry.insert(0, "20")
        threshold_entry.pack(pady=5)
        
        def check():
            drive = drive_entry.get()
            threshold = int(threshold_entry.get())
            total, used, free = shutil.disk_usage(drive)
            free_percentage = (free / total) * 100
            result = f"Drive: {drive}\nFree Space: {free_percentage:.2f}%\n"
            if free_percentage < threshold:
                result += f"⚠️ Warning: Free space on {drive} is below {threshold}%!"
            else:
                result += f"✅ Disk space is sufficient on {drive}."
            self.write_output(result)
            dialog.destroy()
        
        ctk.CTkButton(
            frame,
            text="Check Space",
            command=check
        ).pack(pady=20)

    def monitor_bandwidth(self):
        counters = psutil.net_io_counters()
        result = f"📡 Network Statistics:\n\n"
        result += f"↑ Bytes Sent: {counters.bytes_sent / (1024 ** 2):.2f} MB\n"
        result += f"↓ Bytes Received: {counters.bytes_recv / (1024 ** 2):.2f} MB"
        self.write_output(result)

    def list_processes(self):
        result = "🔄 Running Processes:\n\n"
        for proc in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
            result += f"PID: {proc.info['pid']}\n"
            result += f"Name: {proc.info['name']}\n"
            result += f"Memory: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB\n"
            result += "------------------------\n"
        self.write_output(result)

    def create_task_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Create Scheduled Task")
        dialog.geometry("500x300")
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("Task Name:", "task_name"),
            ("Script Path:", "script_path"),
            ("Time (HH:MM):", "time")
        ]
        
        entries = {}
        for label_text, key in fields:
            ctk.CTkLabel(frame, text=label_text).pack(pady=5)
            entry = ctk.CTkEntry(frame, width=300)
            entry.pack(pady=5)
            entries[key] = entry
        
        def create():
            try:
                command = f"schtasks /create /tn {entries['task_name'].get()} "
                command += f"/tr {entries['script_path'].get()} "
                command += f"/sc once /st {entries['time'].get()}"
                subprocess.run(command, shell=True, check=True)
                self.write_output(f"✅ Task '{entries['task_name'].get()}' created successfully!")
            except Exception as e:
                self.write_output(f"❌ Failed to create task: {e}")
            dialog.destroy()
        
        ctk.CTkButton(
            frame,
            text="Create Task",
            command=create
        ).pack(pady=20)

    def collect_inventory(self):
        result = "🖥️ System Information:\n\n"
        result += f"OS: {platform.system()} {platform.release()}\n"
        result += f"CPU: {platform.processor()}\n"
        result += f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        result += f"Storage: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB"
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
                
                self.write_output(f"✅ Logs archived to {archive_path}.zip\n📤 Old logs removed")
            except Exception as e:
                self.write_output(f"❌ Error: {e}")

    def find_duplicates_dialog(self):
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            result = "🔍 Duplicate Files:\n\n"
            seen = {}
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = self.hash_file(file_path)
                    if file_hash in seen:
                        result += f"Found duplicate:\n{file_path}\n↔️\n{seen[file_hash]}\n\n"
                    else:
                        seen[file_hash] = file_path
            self.write_output(result if len(result) > 25 else "✅ No duplicates found!")

    def hash_file(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def track_user_sessions(self):
        result = "👥 Active User Sessions:\n\n"
        for session in psutil.users():
            result += f"User: {session.name}\n"
            result += f"Terminal: {session.terminal}\n"
            result += f"Started: {datetime.fromtimestamp(session.started)}\n"
            result += "------------------------\n"
        self.write_output(result)

def main():
    app = ModernITSupportGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
