ARG PY_VER="3.6"
FROM python:${PY_VER}

LABEL maintainer="Clooooode<jackey8616@gmail.com>"

COPY ./yunnms /YunNMS/yunnms
COPY ./data /YunNMS/data
COPY ./requirements.txt /YunNMS/requirements.txt

WORKDIR /YunNMS

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m", "yunnms"]

CMD ["-as", "127.0.0.1:8000"]
