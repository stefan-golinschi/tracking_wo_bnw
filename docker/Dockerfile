FROM nvidia/cuda:9.0-devel-ubuntu16.04

ENV USERNAME="user"
ENV MINICONDA_VERSION 4.7.12
ENV MINICONDA_ENV="tracking_wo_bnw"
ENV PYTHON_VERSION="3.6.9"

ENV CPATH="/usr/local/cuda-9.0/include"
ENV CUDA_PATH=/usr/local/cuda-9.0
ENV PATH=/usr/local/cuda-9.0/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64:$LD_LIBRARY_PATH
ENV CFLAGS=-I/usr/local/cuda-9.0/include
ENV LDFLAGS=-L/usr/local/cuda-9.0/lib64

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
  libglib2.0-0 libsm6 libfontconfig1 libxrender1 libxext6

RUN apt-get install -y --no-install-recommends \
    tmux git vim sudo aria2

# add user
RUN useradd -G video -ms /bin/bash ${USERNAME} \
  && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
  && chmod 0440 /etc/sudoers.d/${USERNAME}


# Install conda under user
USER ${USERNAME}
RUN \
  aria2c \
    --max-concurrent-downloads=16 \
    --max-connection-per-server=16 \
    --min-split-size=2M --split=16 \
    -d /tmp https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
  && /bin/bash /tmp/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -b -p /home/${USERNAME}/miniconda3 \
  && sudo rm -f /tmp/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
  && echo '. ${HOME}/miniconda3/etc/profile.d/conda.sh' >> /home/user/.bashrc \
  && . ${HOME}/miniconda3/etc/profile.d/conda.sh \
  && conda clean -ay

USER ${USERNAME}
RUN \
  . ${HOME}/miniconda3/etc/profile.d/conda.sh \
  && cd ${HOME} \
  && conda create -n ${MINICONDA_ENV} python=${PYTHON_VERSION}

USER ${USERNAME}
RUN mkdir -p /home/user/Downloads
COPY resources/torch-0.3.1-cp36-cp36m-linux_x86_64.whl /home/user/Downloads/torch-0.3.1-cp36-cp36m-linux_x86_64.whl

RUN \
  cd ${HOME} \
  && git clone \
    --recurse-submodules \
    --branch master \
    https://github.com/phil-bergmann/tracking_wo_bnw.git \
  && cd tracking_wo_bnw \
  && . ${HOME}/miniconda3/etc/profile.d/conda.sh \
  && conda activate ${MINICONDA_ENV} \
  && pip install -r requirements.txt \
  && pip install -e src/fpn \
  && pip install -e src/frcnn \
  && pip install -e . \
  && pip install /home/user/Downloads/torch-0.3.1-cp36-cp36m-linux_x86_64.whl

RUN \
  cd ${HOME}/tracking_wo_bnw \
  && . ${HOME}/miniconda3/etc/profile.d/conda.sh \
  && conda activate ${MINICONDA_ENV} \
  && sh src/fpn/fpn/make.sh \
  && sh src/frcnn/frcnn/make.sh

  
USER ${USERNAME}
RUN \
  echo 'conda activate ${MINICONDA_ENV}' >> /home/user/.bashrc

WORKDIR /home/user/tracking_wo_bnw
