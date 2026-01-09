import os
from datetime import date, datetime, timedelta
from google.cloud import storage

SA_PATH = os.getenv("SA_PATH")

if SA_PATH and SA_PATH.endswith(".json"):
    client = storage.Client.from_service_account_json(SA_PATH)
else:
    client = storage.Client()

def generate_signed_url(gcs_path: str, expiration_minutes: int = 60) -> str:
    """
    gcs_path: 'gs://bucket_name/path/to/file.png'
    expiration_minutes: duración del URL firmado
    """
    if not gcs_path.startswith("gs://"):
        return None

    path_parts = gcs_path[5:].split("/", 1)
    bucket_name = path_parts[0]
    blob_name = path_parts[1]

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))
    return url

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

def convert_to_geojson(rows, lat_field="latitude", lon_field="longitude", id_field="id"):
    """
    Convierte una lista de registros serializados a GeoJSON.
    """
    features = []
    for r in rows:
        try:
            lat = float(r[lat_field])
            lon = float(r[lon_field])
        except (KeyError, TypeError, ValueError):
            continue  # saltar registros sin coordenadas válidas

        feature = {
            "type": "Feature",
            "id": r.get(id_field),
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": {k: v for k, v in r.items() if k not in [lat_field, lon_field, id_field]},
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }