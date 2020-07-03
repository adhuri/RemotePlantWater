import atexit
import logging
from devices.motor import Motor
from logger import init_logger
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, abort, jsonify
from multiprocessing import Process

# Init logger
init_logger()
logger = logging.getLogger("water_plants")


# Init Motors with bcm pin numbers. The name is useful for configs
m1 = Motor(name="Motor Indoor", bcm_pin_number=17)
m2 = Motor(name="Motor Outdoor", bcm_pin_number=27)

active_motors = [m1, m2]

# Scheduler
sched = BackgroundScheduler()

for m in active_motors:
    schedule_times = m.get_schedule()
    logger.info(f"Scheduled times {str(schedule_times)} for motor {m.name}")
    for hour_to_run, minute_to_run, second_to_run in schedule_times:
        sched.add_job(m.run, trigger='cron', hour=hour_to_run,
                  minute=minute_to_run, second=second_to_run)

sched.start()

# Init Display if it exists
try:
    from display.timestamp_display import Display
    logger.info("Starting the display")
    dis = Display()
    display_process = Process( 
            name = "waterplant_display",
            target=dis.fill,
            args=(),
            daemon = True)
    display_process.start()


except ModuleNotFoundError:
    logger.warning("No Display connected. Mocking display")
except Exception as e:
    logger.error(f"Display process had issues {e}")

# Routes
app = Flask(__name__)
@app.route("/")
def home():
    with open('config.ini', 'r') as f:
        content = f.read()
        headers = {'Content-Type': 'text/html'}
        return render_template('index.html', content=content, headers=headers)


@app.route("/<motor>/water", methods=['GET'])
def water_now(motor: str):
    # Private method to plant water once
    def _plant_water_once(m: Motor, duration: str):
        m.start(duration=duration)
        m.stop()
    # Select Motor
    if motor.lower() == "indoor":
        m = m1
    elif motor.lower() == "outdoor":
        m = m2
    else:
        abort(404, description="Motor not found. Options are indoor or outdoor")

    # Daemon process
    duration = request.args.get(
        'duration', default=m.default_pump_duration(), type=int)
    heavy_process = Process(  # Create a daemonic process
        target=_plant_water_once,
        args=(m, duration,),
        daemon=True)
    heavy_process.start()
    return jsonify(message="Processing the request to water the motor", device=m.name, duration=f"{duration} seconds")


@app.route("/stats", methods=['GET'])
def get_count_dict():
    stats_dict = {m.name: {"today": m.db.get_today_count(), "total": m.db.get_total_count(
    ), "last_watered": m.db.get_last_timestamp()} for m in active_motors}
    return jsonify(stats_dict)


atexit.register(lambda: sched.shutdown())

for m in active_motors:
    atexit.register(m.cleanUpGPIO)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
