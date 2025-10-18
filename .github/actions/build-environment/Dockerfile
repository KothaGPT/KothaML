FROM khulnasoft/build-environment:0.6.18 as builder

# Install Java
ARG JAVA_VERSION=1.15.0-openjdk-amd64
RUN \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-${JAVA_VERSION} && \
    rm -rf /var/lib/apt/lists/*

# Install docker-compose
ARG DOCKER_COMPOSE_VERSION=1.28.5
RUN \
    curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install kind for Kubernetes testing
ARG KIND_VERSION=0.9.0
RUN \
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v${KIND_VERSION}/kind-linux-amd64 && \
    chmod +x ./kind && \
    mv ./kind /usr/local/bin/kind
COPY kind-config.yaml /kind-config.yaml

# Install kubectl
ARG KUBECTL_VERSION=v1.18.12
RUN \
    curl -Lo ./kubectl https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Install lib required for psycopg2
RUN \
    apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Update node and yarn version
ARG NODE_VERSION=16.x
RUN \
    apt-get update && \
    curl -sL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g yarn@1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY extended-entrypoint.sh /extended-entrypoint.sh

RUN chmod +x /extended-entrypoint.sh

FROM builder as final

RUN chmod +x /extended-entrypoint.sh

ENTRYPOINT ["/tini", "-g", "--", "/extended-entrypoint.sh"]
