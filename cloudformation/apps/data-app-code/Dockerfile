FROM python:3.9.5-slim

WORKDIR /app

COPY ./code/app.py /app
COPY ./code/requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade cython
RUN pip3 install -r requirements.txt

CMD [ "streamlit", "run", "app.py", "--server.port", "80" ]