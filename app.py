from flask import Flask, render_template, request, redirect, flash, session, send_file, send_from_directory
from marksheetI import MarksheetI
from marksheetII import MarksheetII
import os
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-marksheet', methods=['GET', 'POST'])
def upload_marksheet():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        marksheet_type = request.form.get('marksheet-type')  # Get the selected marksheet type

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File uploaded successfully')
            session['file_path'] = file_path
            session['marksheet_type'] = marksheet_type  # Store the marksheet type in session

            # Redirect to the success page after successful upload
            return redirect('/success')  

    return render_template('index.html')

@app.route('/success')
def success():
    marksheet_type = session.get('marksheet_type')
    if marksheet_type == 'marksheet-I':
        filename = 'marksheet-I.csv'
    elif marksheet_type == 'marksheet-II':
        filename = 'marksheet-II.csv'
    else:
        filename = ''  # Set a default filename or handle the case where marksheet type is not set
    renamed_filename = session.get('renamed_filename', filename)  # Get the renamed filename from the session
    return render_template('success.html', filename=filename, renamed_filename=renamed_filename)


@app.route('/generate-csv', methods=['POST'])
def generate_csv():
    file_path = session.get('file_path')
    marksheet_type = session.get('marksheet_type')

    if not file_path:
        flash('No file uploaded')
        return redirect(request.url)

    if not marksheet_type:
        flash('No marksheet type selected')
        return redirect(request.url)

    if marksheet_type == 'marksheet-I':
        marksheet_I = MarksheetI(file_path)
        output_path = 'output_data/marksheet-I.csv'
        marksheet_I.save_data_to_csv(['PRN', "STUDENT'S NAME", "ENGINEERING MATHEMATICS", 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering', 'SGPA', 'CGPA'])
        session['renamed_filename'] = 'marksheet-I.csv'  # Set the renamed filename in the session
        flash('File data added successfully')
        return redirect('/view-csv')
    elif marksheet_type == 'marksheet-II':
        marksheet_II = MarksheetII(file_path)
        output_path = 'output_data/marksheet-II.csv'
        marksheet_II.save_data_to_csv(['PRN', "STUDENT'S NAME", 'Engineering Mathematics-II', 'Engineering Physics', 'Engineering Graphics', 'Energy and Environment Engineering', 'Basic Civil and Mechanical Engineering', 'Seminar'])
        session['renamed_filename'] = 'marksheet-II.csv'  # Set the renamed filename in the session
        flash('File data added successfully')
        return redirect('/view-csv')

@app.route('/view-csv')
def view_csv():
    file_path = session.get('file_path')
    marksheet_type = session.get('marksheet_type')

    if not file_path:
        flash('No file uploaded')
        return redirect(request.url)

    if not marksheet_type:
        flash('No marksheet type selected')
        return redirect(request.url)

    csv_data = []  # Initialize an empty list to store CSV data
    csv_filename = session.get('renamed_filename', '')  # Get the renamed filename from the session

    if marksheet_type == 'marksheet-I':
        with open('output_data/marksheet-I.csv', 'r') as csv_file:
            csv_data = list(csv.reader(csv_file))  # Read all rows of the CSV file
            csv_filename = 'marksheet-I.csv'  # Example filename, replace it with the actual generated filename
    elif marksheet_type == 'marksheet-II':
        with open('output_data/marksheet-II.csv', 'r') as csv_file:
            csv_data = list(csv.reader(csv_file))  # Read all rows of the CSV file
            csv_filename = 'marksheet-II.csv'  # Example filename, replace it with the actual generated filename
    else:
        flash('Invalid marksheet type')
        return redirect(request.url)

    return render_template('view_csv.html', csv_data=csv_data, filename=csv_filename)


@app.route('/download-csv', methods=['POST'])
def download_csv():
    new_filename = request.form.get('new_filename')
    file_path = session.get('file_path')

    if new_filename:
        # Rename the file
        filename = os.path.basename(file_path)
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        os.rename(file_path, new_file_path)
        return send_file(new_file_path, as_attachment=True, download_name=new_filename)
    else:
        filename = os.path.basename(file_path)
        renamed_filename = session.get('renamed_filename', filename)  # Get the renamed filename from the session
        return send_file(file_path, as_attachment=True, download_name=renamed_filename)


if __name__ == '__main__':
    app.run(debug=True)
