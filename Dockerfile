FROM python:3.13-slim

WORKDIR /dating-app-for-animal-adoption

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "datingapp.py"]