from flask import Flask,request

app = Flask(__name__)

@app.route("/recognition",methods=['POST'])
def hello():
    print(request.form)
    print(request.form.get('name'))
    print(request.form.get('img'))
    return "Hello world!"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8888,debug=True)
