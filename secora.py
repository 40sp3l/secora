# secora is a bug bounty automation framework
import requests
from colorama import Fore
from art import text2art
import readline
from subprocess import check_output
import os
import time
import queue
import threading
import subprocess
from typing import Dict, Tuple

# unix only
if os.name == "posix":
   os.system('clear')
else:
   exit()

# banner
print(text2art("secora"))
print(Fore.YELLOW+"[SECORA]: A Bug Bounty Hunter's Terminal ------> [CREATOR]: @40sp3l\n"+Fore.WHITE)
# help
print(Fore.BLUE+"[+] Help: "+Fore.WHITE)
print(Fore.BLUE+"Command: list sessions -------> List All Sessions"+Fore.WHITE)
print(Fore.BLUE+"Command: interact <session_id> -------> Interact With The Session"+Fore.WHITE)
print(Fore.BLUE+"Command: Exit -------> Exit Secura\n"+Fore.WHITE)

# Dictionary to store background processes and their details
background_tasks: Dict[int, Tuple[subprocess.Popen, str, queue.Queue]] = {}
task_counter = 0

def run_subfinder_command(command: str, task_id: int) -> None:
    """Run a subfinder command in the background and capture output."""
    process = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output_queue = queue.Queue()
    background_tasks[task_id] = (process, command, output_queue)

    # Thread to capture output
    def capture_output():
        while process.poll() is None:
            line = process.stdout.readline()
            if line:
                output_queue.put(line.strip())
        # Capture any remaining output
        for line in process.stdout:
            if line:
                output_queue.put(line.strip())

    threading.Thread(target=capture_output, daemon=True).start()

def list_sessions() -> None:
    """List all running background tasks."""
    if not background_tasks:
        print("\n[!] No background tasks running.\n")
        return

    print("\nBackground Tasks:")
    for task_id, (_, command, _) in background_tasks.items():
        print(f"\nID: {task_id} | Command: {command}\n")

def interact_task(task_id: int) -> None:
    """Display the output of a specific background task."""
    if task_id not in background_tasks:
        print(f"\n[!] No task found with ID {task_id}\n")
        return

    process, command, output_queue = background_tasks[task_id]
    print(f"\nInteracting with task ID {task_id} | Command: {command}\n")

    # Print any queued output
    while not output_queue.empty():
        print(output_queue.get())

    # Check if process is still running and display new output
    while process.poll() is None:
        try:
            line = output_queue.get(timeout=1)
            print(line)
        except queue.Empty:
            continue

    # Print any remaining output after process completion
    while not output_queue.empty():
        print(output_queue.get())

    print(f"\nTask ID {task_id} has completed.\n")

def main():
    global task_counter
    while True:
        user_input = input(Fore.YELLOW+"[SECORA]-------> "+Fore.WHITE).strip()
        
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        if user_input.startswith("subfinder") or user_input.startswith("assetfinder") or user_input.startswith("nmap") or user_input.startswith("httpx-toolkit") or user_input.startswith("curl") or user_input.startswith("amass") or user_input.startswith("waybackurls") or user_input.startswith("gau") or user_input.startswith("findomain") or user_input.startswith("gf") or user_input.startswith("meg") or user_input.startswith("nuclei") or user_input.startswith("dalfox") or user_input.startswith("sqlmap") or user_input.startswith("dirsearch") or user_input.startswith("ffuf") or user_input.startswith("gobuster") or user_input.startswith("arjun") or user_input.startswith("ksubdomain") or user_input.startswith("wafw00f") or user_input.startswith("whatweb") or user_input.startswith("naabu") or user_input.startswith("cat") or user_input.startswith("httprobe") or user_input.startswith("anew") or user_input.startswith("grep"):
            task_counter += 1
            print(f"\nStarting task ID {task_counter} in the background\n")
            threading.Thread(
                target=run_subfinder_command,
                args=(user_input, task_counter),
                daemon=True
            ).start()
            time.sleep(0.1)

        elif user_input == "list sessions":
            list_sessions()

        elif user_input.startswith("interact "):
            try:
                task_id = int(user_input.split(" ")[1])
                interact_task(task_id)
            except (IndexError, ValueError):
                print("\n[!] Invalid command. Use: interact <background_ID>\n")

        else:
            print("\n[!] Unknown command. Supported commands: subfinder <args>, list sessions, interact <ID>, exit\n")

if __name__ == "__main__":
    main()
