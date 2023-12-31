import subprocess

def run_request_script(num_times):
    script_name = "request-script-v1.1.py"
    processes = []

    try:
        for _ in range(num_times):
            process = subprocess.Popen(["python", script_name])
            processes.append(process)

        # Wait for all child processes to finish
        for process in processes:
            process.wait()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        num_times = int(input("Enter the number of times to run the script: "))
        run_request_script(num_times)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
