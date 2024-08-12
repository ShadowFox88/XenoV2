FROM python:bullseye

WORKDIR /main

COPY requirements.txt .

RUN pip install -Ur requirements.txt

RUN git config --global --add safe.directory /main

COPY . .

CMD ["python", "main.py"]