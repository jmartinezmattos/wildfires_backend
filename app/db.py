import mysql.connector
from .utils import serialize_row, convert_to_geojson


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

    def fetch_table_to_geojson(self, table):

        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)

        sql = f"SELECT * FROM {table}"

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        serialized_rows = [serialize_row(r) for r in rows]
        geo_jsons = convert_to_geojson(serialized_rows)

        return geo_jsons

    def fetch_between_dates(self, table, start_date, end_date, fire=False):
        """
        Devuelve los registros de la tabla entre dos fechas.
        Convierte datetime / date / timedelta a string para JSON.
        """

        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)

        sql = f"SELECT * FROM {table} WHERE firms_datetime BETWEEN %s AND %s"
        params = [start_date, end_date]

        if fire:
            sql += " AND prediction = %s"
            params.append("Fire")

        sql += " ORDER BY firms_datetime ASC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        serialized_rows = [serialize_row(r) for r in rows]
        geo_jsons = convert_to_geojson(serialized_rows)

        return geo_jsons