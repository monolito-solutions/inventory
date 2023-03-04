FROM python:3.10

EXPOSE 5001/tcp

COPY requirements.txt /.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]