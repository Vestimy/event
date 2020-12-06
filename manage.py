# from event import manager
from event import create_app
from event import db

app = create_app()
app.app_context().push()
db.create_all(app=create_app())
security = app.extensions.get('security')
client = app.test_client()





if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')