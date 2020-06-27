from water_plant_flask import app

# uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads
if __name__ == "__main__":
    app.run()
