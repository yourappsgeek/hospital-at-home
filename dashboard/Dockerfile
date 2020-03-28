FROM python:3.6.1

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5006

CMD bokeh serve --disable-index-redirect --num-procs=4 --port=5006 --address=0.0.0.0 --allow-websocket-origin=$DASHBOARD_DEMO_DOMAIN app.py
