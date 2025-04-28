import csv
import os
import sys

def test_write_csv():
    try:
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Test writing to a simple file first
        with open('test_permission.txt', 'w') as f:
            f.write('Test write permission')
        print("Test file created successfully")
        
        # Now try writing to the CSV file
        csv_file_path = os.path.join(os.getcwd(), 'submissions.csv')
        print(f"Attempting to write to: {csv_file_path}")
        
        # Check if the file exists
        file_exists = os.path.isfile(csv_file_path)
        print(f"File already exists: {file_exists}")
        
        # Write to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Email", "Phone"])
            writer.writerow(["Test User", "test@example.com", "1234567890"])
        
        print(f"CSV file written successfully")
        
        # Verify file exists
        if os.path.exists(csv_file_path):
            print(f"File exists with size: {os.path.getsize(csv_file_path)} bytes")
        else:
            print("ERROR: File does not exist after write operation")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_write_csv() 