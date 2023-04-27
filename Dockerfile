FROM debian

RUN mkdir pattern
RUN mkdir results
RUN mkdir target
RUN mkdir config
RUN mkdir pre
RUN mkdir __pycache__

COPY LICENSE .
COPY main.py .
COPY README.md .
COPY requirements.txt .
COPY config /config/
COPY pre /pre/

RUN apt-get update && apt-get upgrade
RUN apt install -y wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev nodejs default-jdk tar openssl
RUN mkdir python && cd python
RUN wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz && tar xzf Python-3.10.8.tgz && cd Python-3.10.8
RUN ./configure --enable-optimizations
RUN make altinstall
RUN cd ..
RUN cd ..
RUN apt install pre/wkhtmltox.deb -y
RUN pip3.10 install -r requirements.txt
RUN python3.10 main.py --mode argm --command install_tools

EXPOSE 5000
EXPOSE 8000
EXPOSE 5555

CMD ["python3.10", "./main.py"]
