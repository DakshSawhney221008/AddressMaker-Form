import csv
import os
import sys
import time

def main():
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    csv_file = os.path.join(os.getcwd(), "submissions.csv")
    print(f"Target CSV file: {csv_file}")
    
    # Check if directory is writable
    dir_writable = os.access(os.getcwd(), os.W_OK)
    print(f"Directory writable: {dir_writable}")
    
    # Check if file exists
    file_exists = os.path.exists(csv_file)
    print(f"File exists: {file_exists}")
    
    # Try writing to the file
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Email", "Phone", "Timestamp"])
            writer.writerow(["Direct Test", "direct@test.com", "9876543210", timestamp])
        print(f"Successfully wrote to CSV file at {csv_file}")
        
        # Verify file size
        print(f"File size after write: {os.path.getsize(csv_file)} bytes")
        
        # Read back contents to verify
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"File content:\n{content}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 