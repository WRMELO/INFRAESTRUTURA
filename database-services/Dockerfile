# Dockerfile base para database-services
# --- database-services Dockerfile ---
FROM postgres:15-alpine

# 1) Variáveis de ambiente padrão (pode sobrescrever no compose)
ENV POSTGRES_USER=ds_user
ENV POSTGRES_PASSWORD=ds_password
ENV POSTGRES_DB=ds_database

# 2) (Opcional) scripts de inicialização SQL/DDL
# Crie um subdiretório initdb/ ao lado se tiver scripts .sql ou .sh
COPY ./initdb /docker-entrypoint-initdb.d

# 3) Porta do Postgres
EXPOSE 5432

