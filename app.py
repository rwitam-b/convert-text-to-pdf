from flask import Flask, render_template, request, send_file

import pdfkit
import os
from datetime import datetime

path_wkhtmltopdf = os.getenv(
    "WKHTMLTOPDF_PATH", "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def convert_to_pdf(source_path, destination_path):
    options = {
        'orientation': 'Landscape',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8"
    }
    pdfkit.from_file(source_path, destination_path, options=options)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def file_upload():
    if request.method == 'POST':
        # Getting present server time
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H%M%S%f")

        # Getting uploaded file details
        f = request.files['statement']

        # Constructing filenames
        input_filename = f.filename + "_" + timestampStr + '.txt'
        output_filename = f.filename + "_" + timestampStr + '.pdf'
        download_filename = f.filename + '.pdf'

        # Saving file and converting to PDF
        f.save(input_filename)
        convert_to_pdf(input_filename, output_filename)
        return send_file(output_filename, as_attachment=True, attachment_filename=download_filename)


if __name__ == "__main__":
    app.run(port=8080)
