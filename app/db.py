import mysql.connector
from mysql.connector import Error
from .utils import serialize_row


class CloudSQLClient:
    def __init__(self, db_config):
        if db_config.get("connection_name"):
            self.config = {
                "user": db_config["user"],
                "password": db_config["password"],
                "database": db_config["database"],
                "unix_socket": f"/cloudsql/{db_config['connection_name']}",
            }
        else:
            self.config = {
                "user": db_config["user"],
                "password": db_config["password"],
                "database": db_config["database"],
                "host": db_config["host"],
                "port": int(db_config["port"]),
            }

    def fetch_between_dates(self, table, start_date, end_date):
        """
        Devuelve los registros de la tabla entre dos fechas.
        Convierte datetime / date / timedelta a string para JSON.
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)

        sql = f"""
        SELECT *
        FROM {table}
        WHERE firms_datetime BETWEEN %s AND %s
        ORDER BY firms_datetime ASC
        """

        cursor.execute(sql, (start_date, end_date))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Serializamos los resultados para JSON
        return [serialize_row(r) for r in rows]
