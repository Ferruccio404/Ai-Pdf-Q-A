from flask import Flask, render_template, request
from utils import process_pdfs, answer_question
import os
from io import BytesIO

app = Flask(__name__)

uploaded_pdfs = []
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    status = None

    if request.method == "POST":
        if 'pdf_files' in request.files:
            files = request.files.getlist('pdf_files')
            file_objects = []
            for pdf in files:
                if pdf.filename:
                    file_obj = BytesIO(pdf.read())
                    file_objects.append(file_obj)
                    uploaded_pdfs.append(pdf.filename)
            if file_objects:
                process_pdfs(file_objects)
                status = f"✅ {len(file_objects)} PDF(s) uploaded and processed."

        elif 'query' in request.form:
            if not uploaded_pdfs:
                status = "⚠️ Please upload PDFs first."
            else:
                query = request.form['query']
                answer = answer_question(query)
                chat_history.append({"question": query, "answer": answer})

        elif 'clear' in request.form:
            uploaded_pdfs.clear()
            chat_history.clear()
            status = "✅ History cleared."

    return render_template("index.html", status=status, uploaded_pdfs=uploaded_pdfs, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)