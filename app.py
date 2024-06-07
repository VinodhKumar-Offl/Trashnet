import os
from flask import Flask, render_template, request
from prediction import predict

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def application():
    answer = None
    error = ""
    image_url = None
    
    if request.method == "POST":
        try:
            file = request.files["image"]
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                print(f"Saved file to {file_path}")
                image_url = f'/static/uploads/{file.filename}'
                result = predict(file_path)
                if result:
                    answer = result
                else:
                    error = "Sorry, something went wrong!"
        except Exception as e:
            error = f"Could not understand: {str(e)}"
            print(f"Error: {e}")
    
    # Clear previous prediction when rendering template
    if request.method == "GET":
        answer = None

    return render_template('index.html', answer=answer, error=error, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
