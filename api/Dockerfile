FROM python:3.11-slim-bullseye

RUN apt-get update -y && ACCEPT_EULA=Y \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get autoremove -y --purge && apt-get autoclean -y \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 10001 --system py \
    && adduser --uid 10000 --system --ingroup py --home /app py

COPY --chown=py:py ./ /app/

RUN chown -Rf py:py /app/

USER py

ENV PATH="${PATH}:/app/.local/bin"

RUN pip3 install --user --no-cache-dir -r /app/requirements.txt

WORKDIR /app

RUN sed -i "s/https:\/\/127.0.0.1:9200\//https:\/\/opensearch:9200\//g" ./config/config.py

EXPOSE 5000

CMD ["/app/app.py"]
