import os
import base64, logging, sys

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

class AppServiceAppLogsHandler(logging.StreamHandler):

    # Map logging levels from Python's logging to App Service App Log levels
    logLevelMap = {'INFO': 'informational', 'WARNING': 'warning', 'ERROR': 'error', 'CRITICAL': 'critical'}

    def emit(self, record):
        self.format(record)
        appSvcLevel = AppServiceAppLogsHandler.logLevelMap.get(record.levelname, 'informational')
        b64message = base64.b64encode(record.getMessage().encode()).decode()
        self.stream.write("x-ms-applog:{l}:base64:{m}\n".format(l=appSvcLevel, m=b64message))

# Configure handlers, one for regular STDOUT and one for STDOUT in the format used by App Service
stdout_handler = logging.StreamHandler(stream=sys.stdout)
appServiceAppLogs_handler = AppServiceAppLogsHandler(stream=sys.stdout)
logging.basicConfig(level=logging.DEBUG, handlers=[stdout_handler, appServiceAppLogs_handler])

app = Flask(__name__)

@app.route('/')
def index():
    print('Request for index page received')
    logging.info(f"Log Entry info")
    logging.warning(f"Log Entry warning")
    logging.error(f"Log Entry error\nwith multi-line\nmessages")
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
