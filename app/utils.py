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