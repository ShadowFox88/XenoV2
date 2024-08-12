FROM python:bullseye

WORKDIR /main

COPY requirements.txt .

RUN pip install -Ur requirements.txt

RUN git config --global --add safe.directory /main

COPY . .

RUN mkdir /root/.ssh

RUN mv Docker-Github-Key /root/.ssh/Docker-Github-Key

RUN eval $(ssh-agent)

RUN chmod 600 /root/.ssh/Docker-Github-Key

RUN ssh-add /root/.ssh/Docker-Github-Key

CMD ["python", "main.py"]