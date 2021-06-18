FROM python:3.7-alpine3.13

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --no-cache-dir

COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/main.py"]
