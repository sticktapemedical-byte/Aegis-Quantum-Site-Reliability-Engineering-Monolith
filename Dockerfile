FROM python:3.11-slim

WORKDIR /aegis

COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN pytest tests/ -q

CMD ["python", "aegis_os.py", "--reviewer-mode"]
