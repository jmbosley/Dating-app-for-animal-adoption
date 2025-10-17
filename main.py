from flask import Flask, render_template, request
from google.cloud import datastore
from google.cloud.datastore.query import And, PropertyFilter

app = Flask(__name__)
datastore_client = datastore.Client()

ACCOUNTS = "accounts"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'phoneNumber', 'password']

# Error Message
ERROR_MISSING_VALUE = "Not all required values were provided"

@app.route("/")
def root():
    return render_template("index.html")

# Create a Public Account
@app.route('/' + ACCOUNTS, methods=['POST'])
def post_businesses():
    # get account info
    content = request.get_json()

    # check if minimum info was provided
    if not (set(MIN_ACCOUNT).issubset(content)):
        return ERROR_MISSING_VALUE, 400
    
    # Create new Account
    new_account = datastore.Entity(key=datastore_client.key(ACCOUNTS))
    new_account.update({
        'firstName': content['firstName'],
        'lastName': content['lastName'],
        'email': content['email'],
        'phoneNumber': content['phoneNumber'],
        'password': content['password']
    })
    datastore_client.put(new_account)
    new_account['id'] = new_account.id
    return ("Account was successfully created!", 201)

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
    
    



