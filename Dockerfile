FROM python:3.9

WORKDIR /DS

COPY . .

RUN apt-get clean && apt-get -y update

RUN apt install python3.9

RUN python3 -m pip install -r requirements.txt

# exposing flask default port to the container
EXPOSE 5000


CMD ["python", "main.py"]



