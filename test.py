import subprocess
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_multiple_times.py <number_of_times> <main.py arguments>")
        sys.exit(1)

    try:
        num_times = int(sys.argv[1])
    except ValueError:
        print("The first argument must be an integer representing the number of times to run main.py.")
        sys.exit(1)

    main_args = sys.argv[2:]

    for _ in range(num_times):
        subprocess.run(['python', 'main.py'] + main_args)

if __name__ == "__main__":
    main()