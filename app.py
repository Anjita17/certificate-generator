from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("form.html")

@app.route('/generate', methods=["POST"])
def generate():
    name = request.form["name"]
    course = request.form["course"]
    date = request.form["date"]

    # Load certificate template
    certificate = Image.open("Certificate.png")

    # Use default fonts
    name_font = ImageFont.load_default()
    course_font = ImageFont.load_default()
    date_font = ImageFont.load_default()

    # Draw text
    draw = ImageDraw.Draw(certificate)

    name_position = (500, 465)
    course_position = (340, 715)
    date_position = (170, 948)

    def draw_centered(draw, text, position, font, fill=(0, 0, 0)):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = position[0] - w // 2
        y = position[1]
        draw.text((x, y), text, fill=fill, font=font)

    draw_centered(draw, name, name_position, name_font)
    draw_centered(draw, course, course_position, course_font)
    draw.text(date_position, date, fill=(0, 0, 0), font=date_font)

    # Output as PDF
    output = io.BytesIO()
    certificate.save(output, format="PDF")
    output.seek(0)

    return send_file(output, download_name=f"certificate_{name}.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

