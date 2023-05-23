import threading
from gitex_attendees import execute_att

def execute_multiple_times():
    file_names = ["file1.csv", "file2.csv", "file3.csv","file4.csv", "file5.csv", "file6.csv","file7.csv", "file8.csv", "file9.csv","file10.csv","file11.csv"]  # List of file names
    loop_starts = [1, 18, 36, 54, 72, 90, 108, 126, 144, 162, 180]  # List of loop counts
    loop_ends = [18, 36, 54, 72, 90, 108, 126, 144, 162, 180, 187]  # List of loop counts
    
    threads = []
    
    for file_name, loop_start, loop_end in zip(file_names, loop_starts, loop_ends):
        thread = threading.Thread(target=execute_att, args=(file_name, loop_start, loop_end))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Run the script
execute_multiple_times()