# RemotePlantWater
Water your plants remotely through Google Assistant ( IFTTT web hooks ). The watering component includes Raspberry Pi, Relay, BreadBoards, Battery. 



## Web Setup 
Use the files in the nginx directory to setup nginx/uwsgi server.
This link describes it well - https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

To check control the uwsgi app - status/stop/start can be used
```
sudo systemctl status remoteplant.service
● remoteplant.service - uWSGI instance to serve remoteplant
   Loaded: loaded (/etc/systemd/system/remoteplant.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2020-06-26 18:44:08 PDT; 4min 25s ago
 Main PID: 16589 (uwsgi)
    Tasks: 3 (limit: 2200)
   Memory: 20.0M
   CGroup: /system.slice/remoteplant.service
           ├─16589 /home/pi/.local/bin/uwsgi --ini nginx/remoteplant.ini
           └─16608 /home/pi/.local/bin/uwsgi --ini nginx/remoteplant.ini
```

    

