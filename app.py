from flask import Flask, jsonify

app = Flask(__name__)

hello_dict = {"Hello": "World!"}

@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaton<br/>"
        f"api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/2011-02-28<br/>"
        f"api/v1.0/2011-02-28/2011-03-05<br/>"
        )



if __name__=="__main__":
    app.run(debug=True)


