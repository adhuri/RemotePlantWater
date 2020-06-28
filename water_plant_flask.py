import atexit
from devices.motor import Motor
from logger import init_logger
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from multiprocessing import Process


init_logger()
m = Motor(name="Motor Indoor", bcm_pin_number=2)

# Scheduler
sched = BackgroundScheduler()
hour_to_run, minute_to_run, second_to_run = m.get_schedule()
sched.add_job(m.run, trigger='cron', hour=hour_to_run,
              minute=minute_to_run, second=second_to_run)
sched.start()

# Routes
app = Flask(__name__)
@app.route("/")
def home():
    with open('config.ini', 'r') as f:
        content = f.read()
        headers = {'Content-Type': 'text/html'}
        return render_template('index.html', content=content, headers=headers)


@app.route("/water", methods=['GET'])
def water_now():
    def plant_water_once(duration):
        m.start(duration=duration)
        m.stop()

    duration = request.args.get(
        'duration', default=m.default_pump_duration(), type=int)
    heavy_process = Process(  # Create a daemonic process
        target=plant_water_once,
        args=(duration,),
        daemon=True)
    heavy_process.start()
    return f"Processing the request to water for duration : {duration} seconds"


atexit.register(lambda: sched.shutdown())
atexit.register(m.cleanUpGPIO)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
