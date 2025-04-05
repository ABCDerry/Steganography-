from flask import Flask, render_template, request, send_file
import os
from stegano.lsb import hide, reveal
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ENCRYPTED_FOLDER = "static/encrypted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    decrypted_message = None  # Default value
    
    if request.method == "POST":
        if "encrypt" in request.form:  # Encrypt action
            image = request.files["image"]
            message = request.form["message"]
            
            if image and message:
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                encrypted_path = os.path.join(ENCRYPTED_FOLDER, "encrypted_" + filename)
                
                image.save(image_path)
                
                # Encrypt the message into the image
                secret_image = hide(image_path, message)
                secret_image.save(encrypted_path)

                return send_file(encrypted_path, as_attachment=True)

        elif "decrypt" in request.form:  # Decrypt action
            encrypted_image = request.files["decrypt_image"]
            
            if encrypted_image:
                filename = secure_filename(encrypted_image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                encrypted_image.save(image_path)

                try:
                    decrypted_message = reveal(image_path)  # Extract hidden message
                except Exception:
                    decrypted_message = "Error: No hidden message found!"

    return render_template("index.html", decrypted_message=decrypted_message)

if __name__ == "__main__":
    app.run(debug=True)
