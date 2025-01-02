from flask import Flask, render_template, request, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    email = request.form['email']
    skills = request.form['skills']
    experience = request.form['experience']
    template_choice = request.form['template']

    if template_choice == 'classic':
        html_content = render_template('classic_resume.html', name=name, email=email, skills=skills, experience=experience)
    elif template_choice == 'modern':
        html_content = render_template('modern_resume.html', name=name, email=email, skills=skills, experience=experience)
    elif template_choice == 'creative':
        html_content = render_template('creative_resume.html', name=name, email=email, skills=skills, experience=experience)
    else:
        return "Invalid template selected", 400


    # Create PDF in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    c.drawString(100, 750, f"Name: {name}")
    c.drawString(100, 730, f"Email: {email}")
    c.drawString(100, 710, f"Skills: {skills}")
    c.drawString(100, 690, f"Experience: {experience}")

    # Add your logic for templates here (for now, just simple text)

    c.showPage()
    c.save()

    pdf_buffer.seek(0)

    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
