from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/encrypt", methods=["POST"])
def encrypt_pdf():
    try:
        base64_pdf = request.json.get('file')
        password = request.json.get('password')

        if not base64_pdf or not password:
            return "Missing 'file' (base64 PDF) or 'password'", 400

        pdf_bytes = base64.b64decode(base64_pdf)
        input_stream = BytesIO(pdf_bytes)

        reader = PdfReader(input_stream)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(user_password=password, owner_password=password)

        output_stream = BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='Encrypted.pdf'
        )

    except Exception as e:
        return f"Encryption failed: {str(e)}", 500

