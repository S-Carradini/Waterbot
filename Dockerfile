FROM python:3.11.7 as app
WORKDIR /application
COPY /application/ /application/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn","-b","0.0.0.0:8000","WaterBot_applicaton:app"," --timeout","60"]