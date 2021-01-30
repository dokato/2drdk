FROM conda/miniconda3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN pip install notebook jupyterlab
RUN conda update --yes -n base -c defaults conda
RUN conda install --yes -c anaconda nb_conda_kernels
RUN conda install --yes tornado

# HDDM requires other version of packages
COPY env_hddm.yml ./
RUN conda config --add channels conda-forge \
    && conda env create -n hddm -f env_hddm.yml \
    && conda install -f -n hddm ipykernel \
    && rm -rf /opt/conda/pkgs/*
ENV PATH /opt/conda/envs/hddm/bin:$PATH
ENV CONDA_DEFAULT_ENV hddm
ENV CONDA_PREFIX /opt/conda/envs/hddm
RUN /bin/bash -c "source activate hddm"

# Tini operates as a process subreaper for jupyter.
# This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter-lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

