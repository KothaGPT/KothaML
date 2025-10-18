ARG ARG_WORKSPACE_BASE_IMAGE="khulnasoft/ml-workspace:latest"
# Build from full flavor of workspace with same version
FROM $ARG_WORKSPACE_BASE_IMAGE

ARG ARG_WORKSPACE_FLAVOR="gpu"
ENV WORKSPACE_FLAVOR=$ARG_WORKSPACE_FLAVOR

USER root

# Install NVIDIA packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gnupg2 \
        curl \
        ca-certificates \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/cuda.list \
    && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        cuda-cudart-11-2=11.2.152-1 \
        cuda-compat-11-2 \
        cuda-libraries-11-2=11.2.2-1 \
        libnpp-11-2=11.3.2.152-1 \
        cuda-nvtx-11-2=11.2.152-1 \
        libcublas-11-2=11.4.1.1043-1 \
        libcusparse-11-2=11.4.1.1152-1 \
        libnccl2=2.8.4-1+cuda11.2 \
        libnccl-dev=2.8.4-1+cuda11.2 \
        libnccl2=2.8.4-1+cuda11.2 \
        libnccl-dev=2.8.4-1+cuda11.2 \
        libcudnn8=8.1.1.33-1+cuda11.2 \
        libcudnn8-dev=8.1.1.33-1+cuda11.2 \
        pytorch=1.9.0+cu111 \
        torchvision=0.10.0+cu111 \
        torchaudio=0.9.0 \
        cupy-cuda112=9.6.0 \
        pycuda=2021.1 \
        gpustat=0.6.0 \
        py3nvml=0.2.6 \
        gputil=1.4.0 \
        scikit-cuda=0.5.3 \
        tensorflow-gpu=2.5.0 \
        onnxruntime-gpu=1.8.0 \
        onnxruntime-training=1.8.0 \
        mxnet-cu112=1.8.0 \
        jax[cuda111]=0.2.12 \
        pygpu \
        lightgbm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /root/.cache/* \
    && rm -rf /tmp/*

# Set environment variables
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# Set NVIDIA environment variables
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.2 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450"

# Set CUDA environment variables
ENV CUDA_VERSION 11.2.2
ENV CUDNN_VERSION 8.1.1.33
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"