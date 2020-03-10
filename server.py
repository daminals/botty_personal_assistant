from os import environ
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify, request, Response, url_for
from settings import APP_STATIC

sched = BackgroundScheduler()
app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
variably = True


def task():
    global variably
    variably = True


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/SomeFunction', methods=['POST'])
def SomeFunction():
    global variably
    variably = False
    forward_message = variably
    return render_template('index.html', forward_message=forward_message);


@app.route('/funky', methods=['POST'])
def funky():
    global variably
    variably = True
    forward_message = variably
    return render_template('index.html', forward_message=forward_message);


@app.route('/monky', methods=['POST'])
def monky():
    forward_message = variably
    print(variably)
    return render_template('index.html', forward_message=forward_message);


sched.add_job(task, 'cron', id='pupil_morn', day_of_week='mon-fri', hour=7)
print('sched set')
sched.print_jobs()


if __name__ == '__main__':
    app.run(environ.get('PORT'))
