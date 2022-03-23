from flask import Flask, render_template, url_for, redirect, request
from colorthief import ColorThief
from PIL import Image
import PIL


COLOR_ERROR = 1

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            data = request.files["image"]
            image = Image.open(data).convert("RGB")
            image.save(r"static/image_processed.jpg")
            return redirect("selected")
        except PIL.UnidentifiedImageError:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/selected")
def selected():
    image = ColorThief("static/image_processed.jpg")
    palette_rgb = image.get_palette(color_count=10, quality=COLOR_ERROR)
    palette_hex = []
    for color in palette_rgb:
        palette_hex.append('#%02x%02x%02x' % color)
    return render_template("selected.html", image="static/image_processed.jpg", colors=palette_hex)


if __name__ == "__main__":
    app.run(debug=True)
