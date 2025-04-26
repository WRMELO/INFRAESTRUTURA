FROM minio/minio:latest

# Credenciais
ENV MINIO_ROOT_USER=admin
ENV MINIO_ROOT_PASSWORD=senhasegura

# Expor portas da API S3 e do Console
EXPOSE 9000 9001

ENTRYPOINT ["minio"]
CMD ["server", "/data", "--console-address", ":9001"]
