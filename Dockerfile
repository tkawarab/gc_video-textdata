FROM python:3.8-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /home/video-textdata
WORKDIR $APP_HOME
RUN mkdir $APP_HOME/temp
COPY . ./

ENV GOOGLE_APPLICATION_CREDENTIALS $APP_HOME/conf/google_app_cred.json
RUN pip install -r requirements.txt

CMD ["python", "/home/video-textdata/index.py"]