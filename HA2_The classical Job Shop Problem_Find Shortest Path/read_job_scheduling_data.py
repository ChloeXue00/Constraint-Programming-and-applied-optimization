def read_job_scheduling_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Extract n and m values from the first line
            if not lines:
                raise ValueError("File is empty")
            try:
                n, m = map(int, lines[0].split())
            except ValueError:
                raise ValueError("First line should contain two integers representing n and m")
            # Extract n and m values from the first line
            # n, m = map(int, lines[0].split())

            # Initialize lists for times and machines
            times = []
            machines = []

            # Read the remaining lines and extract times and machines data
            for line in lines[1:]:
                data = list(map(int, line.split()))
                if len(data) % 2 != 0:
                    raise ValueError("Each job line must have an even number of integers")
                machine_process_pairs = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
                machines.append([pair[0] for pair in machine_process_pairs])
                times.append([pair[1] for pair in machine_process_pairs])

            return n, m, times, machines
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except ValueError as ve:
        print(f"Error: {ve}")
        return None

# Entry point of the script
if __name__ == "__main__":
    # Specify the file name (without full path) in the same directory as the script
    file_name = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft06.txt'

    # Construct the full file path by combining the current directory and the file name
    file_path = file_name

    # Read job scheduling data from the specified file
    n, m, times, machines = read_job_scheduling_data(file_path)

    # print the data to stdout
    print("n = {}".format(n))       # jobs (row count)
    print("m = {}".format(n))       # machines (column count)
    print("machines = {}".format(machines))
    print("times = {}".format(times))