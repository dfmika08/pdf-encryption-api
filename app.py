from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import base64

app = Flask(__name__)  # ← This must come before the route decorator

@app.route("/encrypt", methods=["POST"])
def encrypt_pdf():
    try:
        # Get the base64-encoded PDF string and password from Salesforce
        base64_pdf = request.json.get('file')
        password = request.json.get('password')

        if not base64_pdf or not password:
            return "Missing 'file' (base64 PDF) or 'password'", 400

        # Decode base64 string to binary PDF bytes
        pdf_bytes = base64.b64decode(base64_pdf)
        input_stream = BytesIO(pdf_bytes)

        # Read the PDF
        reader = PdfReader(input_stream)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Encrypt the PDF with the provided password
        writer.encrypt(user_password=password, owner_password=password)

        # Write the encrypted PDF to an output stream
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

if __name__ == "__main__":
    app.run(debug=True)
