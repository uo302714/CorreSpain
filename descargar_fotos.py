"""
=============================================================
  CorreSpain - Descargador de fotos de Google Street View
=============================================================

USO:
  1. Ve a https://console.cloud.google.com
     - Crea proyecto - habilita "Street View Static API"
     - Credenciales - Crear clave de API
  2. Ejecuta:  python descargar_fotos.py TU_API_KEY
  3. Espera ~5 minutos
  4. Resultado: carpeta 'fotos/' con spot_1.jpg ... spot_300.jpg

COSTE: ~$2.10 por las 300 fotos (una sola vez, nunca mas)
"""

import sys, os, json, time

try:
    import requests
except ImportError:
    print("Necesitas instalar requests: pip install requests")
    sys.exit(1)

CARPETA_FOTOS = "fotos"
PAUSA = 0.2

SPOTS = [
    (1, "Paseo del Muro de San Lorenzo", 43.5403247, -5.6489271, 304),
    (2, "Senda Costera Gijon-Candas", 43.5464168, -5.6023304, 320),
    (3, "Playa de Poniente", 43.5410593, -5.6718341, 14),
    (4, "Parque de los Pericones", 43.5262154, -5.6569871, 212),
    (5, "Parque de Invierno", 43.3532305, -5.8496973, 208),
    (6, "Senda del Oso", 43.2151643, -6.037013, 339),
    (7, "Senda Fluvial del Nalon", 43.3310168, -5.9295798, 304),
    (8, "Ruta del Cares", 43.2578512, -4.8344437, 202),
    (9, "Lagos de Covadonga", 43.2742914, -4.9862323, 17),
    (10, "Senda Costera de Llanes", 43.4298972, -4.7916445, 226),
    (11, "Playa de Torimbia", 43.4414884, -4.8516779, 223),
    (12, "Parque de Ferrera", 43.5529311, -5.9228758, 233),
    (13, "Paseo de la Ria de Aviles", 43.5529229, -5.9056519, 250),
    (14, "Monte Naranco", 43.3860446, -5.8664675, 286),
    (15, "Playa de Rodiles", 43.5281436, -5.385215, 11),
    (16, "Paseo Maritimo de A Coruna", 43.3800508, -8.4085678, 277),
    (17, "Torre de Hercules Circuit", 43.3861742, -8.4060534, 143),
    (18, "Islas Cies - Ruta del Faro", 42.2194851, -8.9076249, 20),
    (19, "Senda del Rio Verdugo", 42.3915919, -8.4936266, 310),
    (20, "Parque de la Alameda Santiago", 42.8768902, -8.5475049, 63),
    (21, "Brañas do Sar", 42.8755751, -8.531256, 220),
    (22, "Paseo Fluvial del Lérez", 42.4484826, -8.6244212, 46),
    (23, "Senda Costera de Baiona", 42.2514788, -8.7993581, 119),
    (24, "Playa de las Catedrales", 43.5539831, -7.1572855, 192),
    (25, "Cañón del Sil", 42.4110327, -7.6323631, 272),
    (26, "Termas de Ourense Riverside", 42.3483554, -7.9173571, 105),
    (27, "Praia de Samil", 42.2088414, -8.7760225, 345),
    (28, "Senda Fluvial de Lugo", 43.0110, -7.5570, 0),  # Introduce la URL cuando la tengas
    (29, "Monte Aloia", 42.0789873, -8.6751154, 210),
    (30, "Ruta de los Faros Costa da Morte", 43.3247912, -8.8182545, 265),

]


def check_coverage(lat, lng, key):
    url = "https://maps.googleapis.com/maps/api/streetview/metadata"
    r = requests.get(url, params={
        "location": f"{lat},{lng}",
        "source": "outdoor",
        "key": key
    }, timeout=10)
    return r.json().get("status") == "OK"


def download_photo(lat, lng, key, filepath, heading=None):
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "600x400",
        "location": f"{lat},{lng}",
        "fov": "100",
        "pitch": "0",
        "source": "outdoor",
        "key": key
    }
    if heading is not None:
        params["heading"] = str(heading)
    r = requests.get(url, params=params, timeout=15)
    if r.status_code == 200 and len(r.content) > 5000:
        with open(filepath, "wb") as f:
            f.write(r.content)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("USO: python descargar_fotos.py TU_API_KEY_DE_GOOGLE")
        print("\nConsigue tu key en: https://console.cloud.google.com")
        print("Habilita: Street View Static API")
        sys.exit(1)

    key = sys.argv[1]
    os.makedirs(CARPETA_FOTOS, exist_ok=True)

    encontradas = 0
    sin_cobertura = 0
    resultados = {}

    print(f"CorreSpain - Descargando fotos de Google Street View")
    print(f"   {len(SPOTS)} spots | Carpeta: {CARPETA_FOTOS}/")
    print(f"   Coste estimado: ~$2.10\n")

    for i, spot in enumerate(SPOTS):
        sid, nombre, lat, lng = spot[0], spot[1], spot[2], spot[3]
        heading = spot[4] if len(spot) > 4 else None
        pct = f"[{i+1}/{len(SPOTS)}]"
        print(f"{pct} {nombre}...", end=" ", flush=True)

        try:
            has_coverage = check_coverage(lat, lng, key)
        except Exception as e:
            print(f"Error: {e}")
            sin_cobertura += 1
            time.sleep(PAUSA)
            continue

        if not has_coverage:
            print("sin cobertura")
            sin_cobertura += 1
            time.sleep(PAUSA)
            continue

        filepath = os.path.join(CARPETA_FOTOS, f"spot_{sid}.jpg")
        try:
            ok = download_photo(lat, lng, key, filepath, heading)
            if ok:
                print("OK")
                encontradas += 1
                resultados[str(sid)] = filepath
            else:
                print("fallo")
                sin_cobertura += 1
        except Exception as e:
            print(f"Error: {e}")
            sin_cobertura += 1

        time.sleep(PAUSA)

    resumen = {
        "total_spots": len(SPOTS),
        "fotos_encontradas": encontradas,
        "sin_cobertura": sin_cobertura,
        "spots": resultados,
    }
    with open("fotos_resultado.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"Completado!")
    print(f"   Fotos descargadas: {encontradas}/{len(SPOTS)}")
    print(f"   Sin cobertura:     {sin_cobertura}/{len(SPOTS)}")
    print(f"   Guardadas en:      {CARPETA_FOTOS}/")
    print(f"   Coste real:        ~${encontradas * 0.007:.2f}")


if __name__ == "__main__":
    main()
