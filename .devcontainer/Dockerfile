FROM ubuntu:20.04

# install utils
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  bash-completion \
  build-essential \
  cmake \
  gdb \
  git \
  pylint3 \
  python3-argcomplete \
  python3-pip \
  nano \
  wget \
  curl \
  srecord \
  python3-opencv \
  libopencv-dev \
  python3-pyqt5 \
  pyqt5-dev-tools \
  qttools5-dev-tools

RUN pip install matplotlib more-itertools==4.1.0 pyqtgraph control maestro-servo pyjoystick pyserial

ARG USERNAME=lulav
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  # [Optional] Add sudo support for the non-root user
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  # Cleanup
  && rm -rf /var/lib/apt/lists/* \
  && echo "source /usr/share/bash-completion/completions/git" >> /home/$USERNAME/.bashrc

# Installing depthai lib
RUN apt-get update && curl -fL https://docs.luxonis.com/install_dependencies.sh | bash
RUN python3 -m pip install depthai
RUN git clone https://github.com/luxonis/depthai-python.git && \
    cd depthai-python/examples && \
    python3 install_requirements.py && \ 
    python3 -m pip install depthai --user

