from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = Flask(__name__)

@app.route("/encrypt", methods=["POST"])
def encrypt_pdf():
    if 'file' not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files['file']
    password = request.form.get('password', 'Curitec2024')  # Default password

    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="encrypted.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
