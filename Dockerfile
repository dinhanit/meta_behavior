FROM python:3.10

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx  # This library provides libGL.so.1

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","api.py"]
