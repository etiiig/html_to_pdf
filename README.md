# html_to_pdf

HTML to PDF transformation function to deploy on Google Cloud Run.

Deployment script (define GCP project ID and region for each environment before):
```bash
python deploy.py -e dev
```

Example of secured call (requirements: google-auth==1.24.0 requests==2.25.1):
```python
import urllib

import google.auth.transport.requests
import google.oauth2.id_token

HTML_TO_PDF_CLOUD_RUN_URL = 'https://html-to-pdf-blablabla.run.app/'

def secured_request_post(url, data):
    auth_req = google.auth.transport.requests.Request()
    target_audience = url
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)

    req = urllib.request.Request(url, data=data.encode())
    req.add_header('Authorization', f'Bearer {id_token}')
    response = urllib.request.urlopen(req)
    return response

def html_to_pdf(html):
    url = HTML_TO_PDF_CLOUD_RUN_URL
    pdf = secured_request_post(url, html).read()
    return pdf

pdf = html_to_pdf('<html><body><h1>Test</h1></body></html>')
```
