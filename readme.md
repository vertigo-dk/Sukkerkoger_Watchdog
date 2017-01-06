## Sukkerkoger_Watchdog
To be installed on raspberry pis running adafruit video player. Sends OSC message with status of running video.

```
/dead/'pi_id'/
```

The content of the message is **0** if video is running and **1** if it isn't.

Raspberry shuts down when it receives message /shutdown on port 7010 + pi_id .

#### Code edits
This was coded in python 3.4 in a virtualenvironment.

Clone git and cd to folder then create virtualenv:

```
virtualenv -p python3 venv
```

Activate virtualenv:

```
source venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Ready to run!!
```
python run.py
```
