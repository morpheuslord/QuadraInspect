FROM python:3.10

RUN mkdir pattern
RUN mkdir results
RUN mkdir target
RUN mkdir config
RUN mkdir pre
RUN mkdir __pycache__

COPY main.py .
COPY README.md .
COPY requirements.txt .
COPY config /config/
COPY pre/wkhtmltox.deb .

RUN apt-get update && apt-get upgrade -y
RUN apt install -y wget build-essential libtinfo-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev nodejs default-jdk tar openssl
RUN apt install /wkhtmltox.deb -y
RUN pip3 install -r requirements.txt
RUN python3 main.py --mode argm --command install_tools

EXPOSE 5000
EXPOSE 8000
EXPOSE 5555

CMD ["python3", "./main.py"]
