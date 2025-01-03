from flask import Flask, render_template, request, make_response
from xhtml2pdf import pisa
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    skills = request.form['skills']
    experience = request.form['experience']
    education = request.form['education']
    template_choice = request.form['template']

    # Select the template to render based on the user's choice
    if template_choice == 'classic':
        html_content = render_template('classic_resume.html', name=name, email=email, phone=phone, address=address, skills=skills, experience=experience, education=education)
    elif template_choice == 'modern':
        html_content = render_template('modern_resume.html', name=name, email=email, phone=phone, address=address, skills=skills, experience=experience, education=education)
    elif template_choice == 'creative':
        html_content = render_template('creative_resume.html', name=name, email=email, phone=phone, address=address, skills=skills, experience=experience, education=education)
    else:
        # If the template choice is invalid, return a proper response
        return make_response("Invalid template selected", 400)

    # Convert HTML content to PDF and return the response
    return html_to_pdf(html_content)

def html_to_pdf(html_content):
    # Create an in-memory bytes buffer to hold the PDF
    pdf_output = io.BytesIO()

    # Create the PDF from HTML content
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_output)

    # Check if PDF creation was successful
    if pisa_status.err:
        return make_response("Error in generating PDF", 500)

    # Move the cursor to the start of the buffer before reading
    pdf_output.seek(0)

    # Create a response and set the appropriate headers to serve the PDF
    response = make_response(pdf_output.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
