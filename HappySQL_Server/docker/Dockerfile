FROM python:3.6-jessie
MAINTAINER Yorick LAUPA <ylaupa@vente-privee.com>

ENV ACCEPT_EULA Y
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y locales

# Getting the locale right.
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

RUN apt-get install -qy \
      curl \
      apt-transport-https \
      unixodbc \
      unixodbc-dev

# Install Microsoft ODBC Driver 13 SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && \
    apt-get install -qy msodbcsql

CMD ["ls"]
