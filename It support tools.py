import os
import psutil
import shutil
import subprocess
import hashlib
from datetime import datetime
import time
import platform

def check_disk_space(drive="C:/", threshold=20):
    total, used, free = shutil.disk_usage(drive)
    free_percentage = (free / total) * 100
    print(f"Drive: {drive}, Free Space: {free_percentage:.2f}%")
    
    if free_percentage < threshold:
        print(f"Warning: Free space on {drive} is below {threshold}%!")
    else:
        print(f"Disk space is sufficient on {drive}.")

def monitor_bandwidth(interval=5):
    counters = psutil.net_io_counters()
    print(f"Bytes Sent: {counters.bytes_sent / (1024 ** 2):.2f} MB, Bytes Received: {counters.bytes_recv / (1024 ** 2):.2f} MB")
    time.sleep(interval)

def list_processes():
    for proc in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
        print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB")

def create_task(task_name, script_path, time="12:00"):
    try:
        command = f"schtasks /create /tn {task_name} /tr {script_path} /sc once /st {time}"
        subprocess.run(command, shell=True, check=True)
        print(f"Scheduled task '{task_name}' created.")
    except Exception as e:
        print(f"Failed to create scheduled task: {e}")

def collect_inventory():
    print("System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Processor: {platform.processor()}")
    print(f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")
    print(f"Disk Space: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB")

def rotate_logs(log_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = f"{log_dir}/archive_{timestamp}.zip"
    
    shutil.make_archive(archive_path, 'zip', log_dir)
    print(f"Logs archived to {archive_path}")
    
    for file in os.listdir(log_dir):
        if file.endswith(".log"):
            os.remove(os.path.join(log_dir, file))
    print("Old logs deleted.")

def find_duplicates(directory):
    seen = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash in seen:
                print(f"Duplicate found: {file_path} and {seen[file_hash]}")
            else:
                seen[file_hash] = file_path

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def track_user_sessions():
    sessions = psutil.users()
    for session in sessions:
        print(f"User: {session.name}, Terminal: {session.terminal}, Started: {session.started}")

def main():
    print("\n--- IT Support Tool Suite ---")
    while True:
        print("\nSelect an option:")
        print("1. Check Disk Space")
        print("2. Monitor Bandwidth")
        print("3. List Processes")
        print("4. Create Scheduled Task")
        print("5. Collect System Inventory")
        print("6. Rotate Logs")
        print("7. Find Duplicate Files")
        print("8. Track User Sessions")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            drive = input("Enter drive letter (e.g., C:/): ")
            threshold = int(input("Enter space threshold percentage: "))
            check_disk_space(drive, threshold)
        elif choice == "2":
            interval = int(input("Enter monitoring interval (seconds): "))
            monitor_bandwidth(interval)
        elif choice == "3":
            list_processes()
        elif choice == "4":
            task_name = input("Enter task name: ")
            script_path = input("Enter script path: ")
            time = input("Enter time (HH:MM): ")
            create_task(task_name, script_path, time)
        elif choice == "5":
            collect_inventory()
        elif choice == "6":
            log_dir = input("Enter log directory path: ")
            rotate_logs(log_dir)
        elif choice == "7":
            directory = input("Enter directory to check for duplicates: ")
            find_duplicates(directory)
        elif choice == "8":
            track_user_sessions()
        elif choice == "9":
            print("Exiting the tool suite. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
