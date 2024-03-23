FROM python:bullseye

WORKDIR /main

COPY requirements.txt .

RUN pip install -Ur requirements.txt

COPY schema.sql .

RUN psql -h postgres -p 5432 -U Xeno -d XenoDB -f schema.sql 

COPY . .

CMD ["python", "main.py"]