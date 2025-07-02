@app.route("/encrypt", methods=["POST"])
def encrypt_pdf():
    try:
        data = request.get_json()  # ⬅️ must be this, not request.form!
        base64_pdf = data.get('file')
        password = data.get('password')

        if not base64_pdf or not password:
            return "Missing 'file' or 'password'", 400

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

        return Response(
            output_stream.read(),
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Encrypted.pdf"}
        )

    except Exception as e:
        return f"Encryption failed: {str(e)}", 500
