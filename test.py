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

    for x in range(num_times):
        print("----------Attempt: %i----------"%(x+1))
        print("----------Attempt: %i----------"%(x+1))
        print("----------Attempt: %i----------"%(x+1))
        print("----------Of     : %i----------"%num_times)
        print("----------Of     : %i----------"%num_times)
        print("----------Of     : %i----------"%num_times)
        subprocess.run(['python', 'main.py'] + main_args)

    print("Testing complete")
    print("Testing complete")
    print("Testing complete")

if __name__ == "__main__":
    main()