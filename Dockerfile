FROM python:3.12-bullseye

WORKDIR APP

RUN apt update -y
RUN apt upgrade -y
RUN apt install git -y
RUN apt install ffmpeg -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .

CMD ["streamlit", "run", "main.py"]