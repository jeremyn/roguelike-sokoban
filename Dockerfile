FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  python3-pip \
  sqlite3 \
  && rm -rf /var/lib/apt/lists/*

# the group and user ids should match the uid and gid of the calling user, from
#   `id` on the host

ARG USERNAME=docker
ARG UID=1000
ARG GID=${UID}

RUN groupadd -g ${GID} -r ${USERNAME} \
  && useradd -u ${UID} -g ${USERNAME} ${USERNAME} \
  && mkdir -p /home/${USERNAME}/.vscode-server/extensions \
  && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} \
  && mkdir /workdir \
  && chown -R ${USERNAME}:${USERNAME} /workdir

USER ${USERNAME}

COPY --chown=${USERNAME}:${USERNAME} requirements-dev.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt \
  && rm /tmp/requirements-dev.txt

WORKDIR /workdir
