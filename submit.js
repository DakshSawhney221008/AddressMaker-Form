document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("realEstateForm");
    console.log("Form script loaded and ready");

    // API endpoint URL from localtunnel
    const API_URL = "https://tired-ghosts-peel.loca.lt";

    // Check immediately if the server is available
    checkServerStatus();

    function checkServerStatus() {
        console.log("Checking server status...");
        fetch(`${API_URL}/`, { 
            method: "GET",
            mode: 'cors'
        })
        .then(response => {
            console.log("Server status check response:", response.status);
            return response.text();
        })
        .then(text => {
            console.log("Server is running:", text);
        })
        .catch(error => {
            console.error("Server check failed:", error.message);
        });
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        console.log("Form submission started");

        // Show loading indicator
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.textContent = "Submitting...";
            submitButton.disabled = true;
        }

        // Create FormData from the form
        const formData = new FormData(form);
        
        // Special handling for checkbox groups (amenities)
        const amenitiesCheckboxes = form.querySelectorAll('input[name="amenities"]:checked');
        if (amenitiesCheckboxes.length > 0) {
            // Remove any existing amenities entry (FormData can have multiple entries with same name)
            formData.delete('amenities');
            // Add each checked value
            amenitiesCheckboxes.forEach(checkbox => {
                formData.append('amenities', checkbox.value);
            });
        }
        
        // Log all form data for debugging
        console.log("Form data being sent:");
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        // Check if server is running first
        fetch(`${API_URL}/submit`, {
            method: "POST",
            body: formData,
            mode: 'cors'
        }).then(response => {
            console.log("Response status:", response.status);
            console.log("Response headers:", response.headers);
            
            return response.text().then(text => {
                console.log("Response text:", text);
                return { ok: response.ok, text: text, status: response.status };
            });
        })
        .then(result => {
            // Reset button
            if (submitButton) {
                submitButton.textContent = "Submit Inquiry";
                submitButton.disabled = false;
            }
            
            if (result.ok) {
                console.log("Submission successful!");
                alert("Form submitted successfully!");
                form.reset();
                window.location.href = 'thank-you.html';
            } else {
                console.error("Server returned an error:", result.status, result.text);
                alert("Something went wrong. Please try again. Error: " + result.text);
            }
        })
        .catch(error => {
            console.error("Error submitting form:", error);
            
            // Reset button
            if (submitButton) {
                submitButton.textContent = "Submit Inquiry";
                submitButton.disabled = false;
            }
            
            alert("Submission failed. Is the server running? Error: " + error.message);
        });
    });
});

