from datetime import date, datetime, timedelta

def serialize_row(row):
        """
        Convierte datetime / date / timedelta a string para JSON
        """
        result = {}
        for k, v in row.items():
            if isinstance(v, (datetime, date)):
                result[k] = v.isoformat()
            elif isinstance(v, timedelta):
                # Convertimos a segundos
                result[k] = int(v.total_seconds())
            else:
                result[k] = v
        return result