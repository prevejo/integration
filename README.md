# Introdução
Este projeto consiste no script de importação de dados do sistema de transporte para a base de dados da solução.


# Dependências
pip install psycopg2

pip install requests


# Execução
O script é inicializado com o comando:

----> python3 main.py

O script obtem os dados do serviço do gestor e insere os mesmos na base de dados local:

--> Addr: localhost

--> User: postgres

--> Pass: postgres

--> db: prevejodb

O arquivo ./start.sh tem como função acionar o script e transportar os dados para uma base remota. Ele:
--> coleta os dados da base local

--> executa o arquivo ./cleanup.sql para remoção de dados existentes na base remota

--> insere os dados na base remota


# Docker
O build do arquivo Dockerfile produz uma imagem que quando executada, aciona o arquivo ./start.sh e realiza todo o processo de importação dos dados.

O parâmetro `EXPORT_TYPE` identifica o destino [ 'db', 'h2', 'dump' ] dos dados importados. Quando não informado o base de dados não é exportada 
e o container se mantém em execução.

`db` sinaliza que os dados devem ser enviados para uma base de dados remota. Na execução do container com a imagem do Dockerfile deve também ser 
passado os parâmetros de ambiente:

DB_ADDR=<endereço da base remota>

DB_PORT=<porta do banco>

DB_NAME=<nome do banco de dados interno>

DB_SCHEMA=<schema onde os dados serão transferidos>

DB_USER=<usuário do banco>

DB_PASS=<senha do banco>

`h2` sinaliza que os dados devem ser exportados para um arquivo .sql capaz de ser utilizado na inicialização de um banco de dados h2. 
Será criado o arquivo `/tmp/data-h2.sql`.

`dump` sinaliza que os dados devem ser exportados para um arquivo .sql resultado de um postgre dump da base de dados formada na importação. 
Será criado o arquivo `/tmp/data-postgis.sql`.

O build da imagem pode ser feito com: `docker build -t integration -f Dockerfile` .

A execução pode se feita com: `docker run -i --name container-integration --env-file env.list -p 127.0.0.1:5432:5432 integration:latest`

Copia de um arquivo exportado pode ser feita com: `docker cp container-integration:/tmp/data-h2.sql .`
