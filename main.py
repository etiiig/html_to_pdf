import logging
import os
import time

from flask import Flask, request, Response
import pdfkit

app = Flask(__name__)


@app.route("/", methods=["POST"])
def html_to_pdf():
    data = request.get_data()
    start_time = time.time()
    pdf = pdfkit.PDFKit(data.decode("utf-8"), 'string').to_pdf()
    logging.info('pdfkit html to pdf: %.0f ms', (time.time() - start_time) * 1000)
    return Response(pdf, mimetype='application/pdf')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
