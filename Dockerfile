FROM python:3
RUN pip install flask

COPY socket_server.py /
COPY level.txt /
COPY test_server.py /

EXPOSE 5000
ENTRYPOINT ["python3", "test_server.py"]