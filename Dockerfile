FROM python:3.9-bullseye

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y ntpdate
RUN dpkg-reconfigure tzdata
# RUN ntpdate pool.ntp.br

ARG APP_USER_NAME
ARG APP_UID
ARG APP_GID
ARG APP_NAME

RUN adduser --uid $APP_UID --shell /bin/zsh --disabled-password --gecos "" $APP_USER_NAME && chown -R $APP_USER_NAME /home/$APP_USER_NAME

RUN pip install pipenv

RUN apt install -y locales libc-bin locales-all
RUN sed -i '/pt_BR.UTF-8/s/^#//g' /etc/locale.gen \
    && locale-gen en_US en_US.UTF-8 pt_BR pt_BR.UTF-8 \
    && dpkg-reconfigure --frontend noninteractive locales \
    && update-locale LANG=pt_BR.UTF-8 LANGUAGE=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8

ENV PIPENV_VENV_IN_PROJECT=True
ENV PIPENV_SITE_PACKAGES=True

ADD Pipfile.lock ./
ADD Pipfile ./

RUN pipenv install --system

USER $APP_USER_NAME

WORKDIR /home/$APP_USER_NAME/$APP_NAME

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure" ]
# CMD [ "gunicorn", "--access-logfile", "-", "--workers", "3", "--bind", "0.0.0.0:8000", "projeto1.wsgi" ]
