
FROM nexus-docker.brgm.fr/brgm/plateformes/common/python-3.11:latest

COPY --chown=${USER_ID}:${USER_ID} src/requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir -i https://nexus.brgm.fr/repository/pypi-all/simple rameau==0.0.8

COPY --chown=${USER_ID}:${USER_ID} entrypoint.sh /app/entrypoint.sh
COPY --chown=${USER_ID}:${USER_ID} src /app/

RUN chmod +x /app/entrypoint.sh