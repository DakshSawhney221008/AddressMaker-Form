# === server.py ===
# This is your backend server. Run this with Python on your laptop.

from flask import Flask, request, redirect, jsonify
import csv
import os
import traceback
from flask_cors import CORS
import sys
import time

app = Flask(__name__)
# Enable CORS for all domains with additional headers
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"], "expose_headers": ["Content-Type"]}})

@app.route('/', methods=['GET'])
def home():
    print("Root endpoint accessed")
    return "Server is running properly!"

@app.route('/api-test', methods=['GET'])
def api_test():
    print("API test endpoint accessed")
    return jsonify({
        "status": "ok",
        "message": "API is working",
        "time": time.time()
    })

# Route to handle form submission from frontend
@app.route('/submit', methods=['POST'])
def handle_form_submission():
    try:
        print("\n=== FORM SUBMISSION RECEIVED ===")
        print(f"Content-Type: {request.content_type}")
        print(f"Form data keys: {list(request.form.keys()) if request.form else 'No form data'}")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        
        # Create a test file first to check permissions
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_write.txt')
        try:
            with open(test_file_path, 'w') as f:
                f.write('This is a test file to verify write permissions - ' + time.strftime("%Y-%m-%d %H:%M:%S"))
            print(f"Successfully wrote test file at: {test_file_path}")
        except Exception as test_e:
            print(f"ERROR writing test file: {str(test_e)}")
            return (f"Error writing to directory: {str(test_e)}", 500)
        
        data = request.form  # Access form data sent via FormData in JS
        if not data:
            print("No form data received!")
            # Try to get data from request body if form data is empty
            try:
                print("Attempting to parse request body...")
                print(f"Request data: {request.data.decode('utf-8') if request.data else 'No data'}")
            except Exception as e:
                print(f"Error parsing request body: {str(e)}")
            return ("No form data received", 400)

        # Extract fields (add more if needed)
        full_name = data.get('fullName', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        contact_method = data.get('contactMethod', '')
        representation = data.get('representation', '')
        inquiry_type = data.get('inquiryType', '')
        property_type = data.get('propertyType', '')
        location = data.get('location', '')
        budget = data.get('budget', '')
        bedrooms = data.get('bedrooms', '')
        bathrooms = data.get('bathrooms', '')
        parking = data.get('parking', '')
        furnishing = data.get('furnishing', '')
        move_in_date = data.get('moveInDate', '')
        living_at_property = data.get('livingAtProperty', '')
        property_loan = data.get('propertyLoan', '')
        amenities = request.form.getlist('amenities')  # Get as list since it could be multiple values
        loan_approval = data.get('loanApproval', '')
        agent_experience = data.get('agentExperience', '')
        additional_notes = data.get('additionalNotes', '')

        print(f"Received form data - Name: {full_name}, Email: {email}, Phone: {phone}")
        
        # Get the absolute path for the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'submissions.csv')
        print(f"Will save to: {csv_file_path}")
        
        # Check directory permissions
        print(f"Current directory: {current_dir}")
        print(f"Directory exists: {os.path.exists(current_dir)}")
        print(f"Directory is writable: {os.access(current_dir, os.W_OK)}")
        
        # Check if file exists
        file_exists = os.path.isfile(csv_file_path)
        print(f"File already exists: {file_exists}")
        
        # Try to create or append to the CSV file
        try:
            print(f"\nAttempting to write to CSV file at: {csv_file_path}")
            with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    print("Creating new CSV file with headers")
                    writer.writerow([
                        "Full Name", "Email", "Phone", "Contact Method", "Representation",
                        "Inquiry Type", "Property Type", "Location", "Budget", "Bedrooms", "Bathrooms",
                        "Parking", "Furnishing", "Move-in Date", "Living at Property", "Property Loan",
                        "Amenities", "Loan Approval", "Agent Experience", "Additional Notes"
                    ])
                
                print(f"Writing data row to CSV: {full_name}, {email}, {phone}")
                row_data = [
                    full_name, email, phone, contact_method, representation,
                    inquiry_type, property_type, location, budget, bedrooms, bathrooms,
                    parking, furnishing, move_in_date, living_at_property, property_loan,
                    ','.join(amenities) if isinstance(amenities, list) else amenities, 
                    loan_approval, agent_experience, additional_notes
                ]
                writer.writerow(row_data)
                print("Data row written successfully")
                
                # Double-check the file was written by reading it back
                print("\nVerifying CSV data by reading back the file:")
                with open(csv_file_path, mode='r', encoding='utf-8') as verify_file:
                    file_content = verify_file.read()
                    print(f"CSV file content preview: {file_content[:200]}...")
                
        except PermissionError as pe:
            print(f"PERMISSION ERROR: {str(pe)}")
            print(f"Current username: {os.getlogin()}")
            print(f"File permissions: {oct(os.stat(csv_file_path).st_mode if os.path.exists(csv_file_path) else 0)}")
            return (f"Permission denied when writing to CSV file: {str(pe)}", 500)
        except Exception as csv_e:
            print(f"CSV WRITE ERROR: {str(csv_e)}")
            print(traceback.format_exc())
            return (f"Error writing to CSV file: {str(csv_e)}", 500)
        
        # Verify the file was created/updated
        if os.path.exists(csv_file_path):
            print(f"File was successfully created/updated at {csv_file_path}")
            print(f"File size: {os.path.getsize(csv_file_path)} bytes")
        else:
            print("ERROR: File was not created!")
            return ("Failed to create the CSV file", 500)
            
        return ("Thank you!", 200)
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        return (f"Error: {str(e)}", 500)

if __name__ == '__main__':
    print(f"Starting server with Python {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Try to write to submissions.csv at startup
    try:
        test_csv = os.path.join(os.getcwd(), 'submissions.csv')
        with open(test_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not os.path.getsize(test_csv):
                writer.writerow(["Full Name", "Email", "Phone"])
        print(f"Successfully wrote to {test_csv} at startup")
    except Exception as e:
        print(f"WARNING: Could not write to submissions.csv at startup: {str(e)}")
    
    # Run the Flask server locally on port 5000 (can be accessed via LAN)
    app.run(host='0.0.0.0', port=5000, debug=True)