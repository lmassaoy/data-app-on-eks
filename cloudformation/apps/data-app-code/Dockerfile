FROM python:3.9.5-slim

WORKDIR /app

COPY ./code/app.py /app
COPY ./code/utils/ /app/utils/
COPY ./code/requirements.txt /app

COPY ./images/covers/stage.txt /app/images/covers/
COPY ./images/*.png /app/images/
COPY ./images/*.gif /app/images/

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade cython
RUN pip3 install -r requirements.txt

CMD [ "streamlit", "run", "app.py", "--server.port", "80" ]