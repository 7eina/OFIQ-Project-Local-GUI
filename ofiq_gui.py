from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, session
import os
import subprocess
import pandas as pd
import io
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong key for security
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")  # Get list of uploaded files
        selected_attributes = request.form.getlist("attributes")  # Get selected attributes

        results = []
        
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # Run OFIQ executable and get results for each file
            result = run_ofiq(file_path)

            # Filter results based on selected attributes
            filtered_result = [attr for attr in result if attr['attribute'] in selected_attributes]

            results.append({
                "filename": file.filename,
                "image_url": url_for('uploaded_file', filename=file.filename),
                "result": filtered_result
            })

        # Store results in session as JSON
        session['results'] = json.dumps(results)  # Convert to JSON string for session storage

        return render_template("results.html", results=results)
    return render_template("index.html")


def run_ofiq(image_path):
    # Set paths to configuration file and executable
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "OFIQ-Project-main", "data", "ofiq_config.jaxn")
    ofiq_exe_path = os.path.join(base_dir, "OFIQ-Project-main", "install_x86_64", "Release", "bin", "OFIQSampleApp.exe")
    
    try:
        # Run OFIQ executable on the image
        result = subprocess.run(
            [ofiq_exe_path, "-c", config_path, "-i", image_path],
            capture_output=True, text=True
        )
        return parse_output(result.stdout)  # Parse and return the result data
    except Exception as e:
        return f"Error: {e}"

def parse_output(output_text):
    # Extract relevant data from OFIQ output
    lines = output_text.splitlines()
    attributes = []

    print("Debugging: Full Output Text")
    print(output_text)  # Print the full output for debugging

    for line in lines:
        if "->" in line:
            try:
                attribute, values = line.split("->")
                raw_score, scalar_score = values.split("scalar:")
                raw_score = raw_score.replace("rawScore:", "").strip()
                scalar_score = scalar_score.strip()
                attributes.append({
                    "attribute": attribute.strip(),
                    "raw_score": raw_score,
                    "scalar_score": scalar_score
                })
                print(f"Parsed Attribute: {attribute.strip()}, Raw Score: {raw_score}, Scalar Score: {scalar_score}")
            except ValueError:
                print(f"Skipping line (couldn't parse): {line}")

    return attributes

@app.route('/download_excel')
def download_excel():
    # Retrieve results from session and decode JSON
    results = json.loads(session.get('results', '[]'))  # Convert back to list from JSON

    # Extract data and convert to pandas DataFrame
    data = {}
    attributes = [attr['attribute'] for attr in results[0]['result']] if results else []
    data['Attribute'] = attributes

    for item in results:
        raw_scores = [attr['raw_score'] for attr in item['result']]
        scalar_scores = [attr['scalar_score'] for attr in item['result']]
        data[f"{item['filename']} - Raw Score"] = raw_scores
        data[f"{item['filename']} - Scalar Score"] = scalar_scores

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an in-memory buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Quality Assessment')
        worksheet = writer.sheets['Quality Assessment']
        worksheet.set_column(0, len(data) - 1, 20)  # Adjust column width for better readability

    output.seek(0)  # Go to the beginning of the buffer

    # Send the file to the user
    return send_file(output, as_attachment=True, download_name='quality_assessment_results.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
