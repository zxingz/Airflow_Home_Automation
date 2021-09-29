import docker
import logging
import sys

if __name__ == '__main__':

    # setting up logger
    logging.basicConfig(stream=sys.stdout,
                        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    # get the docker client
    client = docker.from_env()

    # list out docker volumes
    logging.info(str([x.name for x in client.volumes.list()]))

    # Check if airflow backend volume is created or not
    # if the volume is not created then create it
    if 'airflow_pg_data' not in [x.name for x in client.volumes.list()]:
        client.volumes.create('airflow_pg_data')

    # kill container if it is already running
    logging.info(str([x.name for x in client.containers.list()]))
    if 'airflow_pg' not in [x.name for x in client.containers.list()]:

        # launch postgres backend
        pg = client.containers.run(image='postgres',
                                   name='airflow_pg',
                                   auto_remove=True,
                                   detach=True,
                                   environment={
                                       'POSTGRES_PASSWORD': 'airflow',
                                       'POSTGRES_USER': 'airflow',
                                       'PGDATA': '/airflow/data'
                                   },
                                   volumes={'airflow_pg_data': {'bind': '/airflow/data', 'mode': 'rw'}},
                                   ports={'5432/tcp': 5432}
                                   )
