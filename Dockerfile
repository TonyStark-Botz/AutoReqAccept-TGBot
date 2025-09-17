FROM python:3.10

EXPOSE 8080

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY . /app
CMD ["python", "bot.py"]
