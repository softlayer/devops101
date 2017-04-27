from dashboard import app
import os
import atexit
app_port = int(os.getenv('VCAP_APP_PORT', '8080'))

@atexit.register
def shutdown():
    print("Shutting Down")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port, debug=False)
