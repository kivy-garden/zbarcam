# Docker image for building Android APKs via buildozer
# Build with:
# docker build --tag=zbarcam-android --file=dockerfiles/Dockerfile-android .
# Run with:
# docker run zbarcam-android /bin/sh -c 'buildozer android debug'
# Or using the entry point shortcut:
# docker run zbarcam-android 'buildozer android debug'
# Or for interactive shell:
# docker run -it --rm zbarcam-android
FROM ubuntu:18.04

ARG CI=false
ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"
ENV DOCKERFILES_VERSION="master" \
    DOCKERFILES_URL="https://raw.githubusercontent.com/AndreMiras/dockerfiles"
ENV MAKEFILES_URL="${DOCKERFILES_URL}/${DOCKERFILES_VERSION}/buildozer_android_new"


# configure locale
RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install system dependencies
RUN apt install -qq --yes --no-install-recommends \
    autoconf \
    automake \
    cmake \
    make \
    ca-certificates \
    curl \
    gettext \
    libffi-dev \
    libltdl-dev \
    libpython3.6-dev \
    libtool \
    file \
    openjdk-8-jdk \
    pkg-config \
    python3.6 \
    python3-setuptools \
    python-pip \
    python-setuptools \
    sudo \
    unzip \
    xz-utils \
    zip

# prepare non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${WORK_DIR}

# install buildozer and dependencies
RUN curl --location --progress-bar ${MAKEFILES_URL}/buildozer.mk --output buildozer.mk
RUN make -f buildozer.mk
# enforces buildozer master (cf880a3) until next release
RUN pip install --upgrade https://github.com/kivy/buildozer/archive/cf880a3.zip

COPY . ${WORK_DIR}
# limits the amount of logs for Travis
RUN if [ "${CI}" = "true" ]; then sed 's/log_level = [0-9]/log_level = 1/' -i buildozer.spec; fi
ENTRYPOINT ["./dockerfiles/start.sh"]
