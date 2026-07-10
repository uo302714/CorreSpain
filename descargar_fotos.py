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
    (1,"Paseo del Muro de San Lorenzo",43.5475,-5.6616),
    (2,"Senda Costera Gijon-Candas",43.5610,-5.6200),
    (3,"Playa de Poniente",43.5390,-5.6870),
    (4,"Parque de los Pericones",43.5250,-5.6350),
    (5,"Parque de Invierno",43.3560,-5.8590),
    (6,"Senda del Oso",43.2280,-5.8950),
    (7,"Senda Fluvial del Nalon",43.3630,-5.8480),
    (8,"Ruta del Cares",43.2530,-4.8350),
    (9,"Lagos de Covadonga",43.2710,-5.0520),
    (10,"Senda Costera de Llanes",43.4210,-4.7550),
    (11,"Playa de Torimbia",43.4450,-4.8530),
    (12,"Parque de Ferrera",43.5570,-5.9230),
    (13,"Paseo de la Ria de Aviles",43.5590,-5.9120),
    (14,"Monte Naranco",43.3720,-5.8700),
    (15,"Playa de Rodiles",43.5310,-5.3870),
    (16,"Paseo Maritimo de A Coruna",43.3710,-8.4060),
    (17,"Torre de Hercules Circuit",43.3860,-8.4060),
    (18,"Islas Cies",42.2310,-8.9050),
    (19,"Senda del Rio Verdugo",42.2960,-8.5370),
    (20,"Parque de la Alameda Santiago",42.8740,-8.5490),
    (21,"Branas do Sar",42.8680,-8.5300),
    (22,"Paseo Fluvial del Lerez",42.4290,-8.6420),
    (23,"Senda Costera de Baiona",42.1170,-8.8490),
    (24,"Playa de las Catedrales",43.5530,-7.1570),
    (25,"Canon del Sil",42.4150,-7.7480),
    (26,"Termas de Ourense Riverside",42.3360,-7.8640),
    (27,"Praia de Samil",42.2120,-8.7720),
    (28,"Senda Fluvial de Lugo",43.0110,-7.5570),
    (29,"Monte Aloia",42.0950,-8.6800),
    (30,"Ruta de los Faros Costa da Morte",43.0520,-9.2150),
    (31,"Paseo do Rio Sar",42.8650,-8.5380),
    (32,"Playa de Carnota",42.8230,-9.1050),
    (33,"Isla de la Toja Circuit",42.4960,-8.8390),
    (34,"Fragas do Eume",43.4230,-8.0870),
    (35,"Cabo Fisterra",42.8830,-9.2720),
    (36,"Paseo del Sardinero",43.4740,-3.7830),
    (37,"Parque de la Magdalena",43.4720,-3.7640),
    (38,"Pena Cabarga",43.3850,-3.8240),
    (39,"Senda Costera de Suances",43.4390,-4.0470),
    (40,"Via Verde del Pas",43.2840,-3.9230),
    (41,"Picos de Europa Fuente De",43.1510,-4.8010),
    (42,"Paseo de Comillas",43.3870,-4.2910),
    (43,"Playa de Berria",43.4590,-3.4630),
    (44,"Monte Buciero",43.4620,-3.4510),
    (45,"Parque Natural de Oyambre",43.3880,-4.3230),
    (46,"Paseo de la Concha",43.3180,-1.9870),
    (47,"Monte Urgull",43.3270,-1.9870),
    (48,"Monte Igueldo",43.3200,-2.0100),
    (49,"Paseo Nuevo San Sebastian",43.3250,-1.9930),
    (50,"Ria del Nervion Bilbao",43.2690,-2.9350),
    (51,"Monte Artxanda",43.2770,-2.9390),
    (52,"Anillo Verde Vitoria",42.8530,-2.6830),
    (53,"Humedales de Salburua",42.8500,-2.6530),
    (54,"Flysch de Zumaia",43.3030,-2.2560),
    (55,"Playa de Zarautz",43.2840,-2.1710),
    (56,"Urdaibai Bosque de Oma",43.3600,-2.6700),
    (57,"Paseo de la Galea",43.3690,-3.0290),
    (58,"GR 38 Ruta del Vino",42.7120,-2.5960),
    (59,"Monte Gorbea",43.0270,-2.7800),
    (60,"Playa de Laga",43.3750,-2.6600),
    (61,"Vuelta del Castillo Pamplona",42.8190,-1.6440),
    (62,"Parques Fluviales del Arga",42.8130,-1.6560),
    (63,"Parque de la Taconera",42.8200,-1.6500),
    (64,"Bardenas Reales",42.2240,-1.5430),
    (65,"Selva de Irati",42.9780,-1.0770),
    (66,"Nacedero del Urederra",42.8060,-2.0850),
    (67,"Foz de Lumbier",42.6490,-1.3090),
    (68,"Camino de Santiago Navarro",42.9310,-1.5680),
    (69,"Embalse de Alloz",42.7540,-1.9770),
    (70,"Sierra de Aralar",42.9650,-1.9520),
    (71,"Parque del Ebro Logrono",42.4640,-2.4460),
    (72,"Pantano de La Grajera",42.4310,-2.4720),
    (73,"Sierra de Cebollera",42.0680,-2.6320),
    (74,"Vinedos de Haro",42.5760,-2.8430),
    (75,"Valle del Najerilla",42.3270,-2.7270),
    (76,"Camino de Santiago Riojano",42.4350,-2.6900),
    (77,"Parque de la Ribera Logrono",42.4660,-2.4390),
    (78,"Penas de Iregua",42.2960,-2.5050),
    (79,"Ribera del Tormes Salamanca",40.9580,-5.6660),
    (80,"Parque de la Aldehuela",40.9520,-5.6490),
    (81,"Ribera del Pisuerga",41.6490,-4.7230),
    (82,"Campo Grande Valladolid",41.6480,-4.7280),
    (83,"Ribera del Bernesga",42.5990,-5.5710),
    (84,"Camino de Santiago Leones",42.5980,-5.5640),
    (85,"Ribera del Eresma Segovia",40.9400,-4.1190),
    (86,"Ruta de los Molinos Segovia",40.9470,-4.1020),
    (87,"Paseo del Espolon Burgos",42.3390,-3.7020),
    (88,"Sendero del Arlanzon",42.3420,-3.6950),
    (89,"Ribera del Duero Soria",41.7640,-2.4640),
    (90,"Dehesa Soriana",41.7590,-2.4490),
    (91,"Canal de Castilla Palencia",42.0130,-4.5300),
    (92,"Canon del Rio Lobos",41.7270,-3.0600),
    (93,"Sierra de Gredos Plataforma",40.2560,-5.2830),
    (94,"Las Medulas",42.4590,-6.7630),
    (95,"Lago de Sanabria",42.1130,-6.7330),
    (96,"Parque de la Isla Burgos",42.3430,-3.6860),
    (97,"Monte Abantos El Escorial",40.5740,-4.1490),
    (98,"Ribera del Tera Zamora",41.5040,-5.7440),
    (99,"Madrid Rio",40.3950,-3.7170),
    (100,"Casa de Campo",40.4170,-3.7490),
    (101,"Parque del Retiro",40.4153,-3.6845),
    (102,"Anillo Verde Ciclista",40.4300,-3.6700),
    (103,"Dehesa de la Villa",40.4530,-3.7200),
    (104,"Parque Juan Carlos I",40.4650,-3.6100),
    (105,"Monte El Pardo",40.5200,-3.7700),
    (106,"Senda Real",40.4900,-3.7500),
    (107,"Parque de Valdebebas",40.4930,-3.6080),
    (108,"Parque Lineal del Manzanares",40.3750,-3.6950),
    (109,"Parque Enrique Tierno Galvan",40.3920,-3.6890),
    (110,"Cerro del Tio Pio",40.3870,-3.6510),
    (111,"Parque Forestal Valdebernardo",40.3780,-3.6120),
    (112,"Canal de Isabel II Senda",40.4860,-3.6900),
    (113,"Sierra de Guadarrama Cercedilla",40.7420,-4.0550),
    (114,"Embalse de Santillana",40.7280,-3.8310),
    (115,"Parque Regional del Sureste",40.3200,-3.5400),
    (116,"Jardin del Capricho",40.4610,-3.6120),
    (117,"Bosque de la Herreria",40.5870,-4.1350),
    (118,"Parque Europa Torrejon",40.4620,-3.4670),
    (119,"Paseo Maritimo Barceloneta",41.3780,2.1920),
    (120,"Carretera de les Aigues",41.4120,2.1280),
    (121,"Montjuic",41.3640,2.1590),
    (122,"Parc del Forum",41.4110,2.2290),
    (123,"Diagonal Mar",41.4090,2.2180),
    (124,"Parc de Collserola",41.4270,2.0990),
    (125,"Tibidabo Trails",41.4220,2.1190),
    (126,"Parc de la Ciutadella",41.3880,2.1870),
    (127,"Canal Olimpic Castelldefels",41.2970,2.0440),
    (128,"Delta del Llobregat",41.3190,2.0750),
    (129,"Cami de Ronda Costa Brava",41.7970,3.0340),
    (130,"GR 92 Cap de Creus",42.3190,3.3160),
    (131,"Paseo de la Muralla Girona",41.9870,2.8260),
    (132,"Devesa de Girona",41.9810,2.8180),
    (133,"Paseo Maritimo Tarragona",41.1100,1.2500),
    (134,"Delta del Ebro",40.6620,0.8690),
    (135,"Serra del Montsant",41.2930,0.8460),
    (136,"Aiguestortes",42.5540,0.9600),
    (137,"Playa de Sitges",41.2350,1.8070),
    (138,"Montserrat",41.5930,1.8380),
    (139,"Parc Natural del Garraf",41.2700,1.8900),
    (140,"Via Verda del Carrilet",41.9550,2.7640),
    (141,"Parc del Turonet",41.3980,2.1290),
    (142,"Cala Montgo L Escala",42.1180,3.1650),
    (143,"Bosc de Can Deu Sabadell",41.5580,2.1200),
    (144,"Passeig de la Mina Terrassa",41.5690,2.0080),
    (145,"Playa de la Pineda",41.0780,1.1770),
    (146,"Serra de l Albera",42.4190,2.9570),
    (147,"Parc de Vallparadis",41.5640,2.0120),
    (148,"Costa Daurada Cambrils",41.0690,1.0600),
    (149,"Jardin del Turia",39.4780,-0.3720),
    (150,"Paseo Maritimo Malvarrosa",39.4780,-0.3260),
    (151,"Albufera de Valencia",39.3350,-0.3500),
    (152,"Parque Natural de la Devesa",39.3250,-0.3200),
    (153,"Parque de Cabecera",39.4760,-0.3960),
    (154,"Serra Gelada Benidorm",38.5420,-0.0830),
    (155,"Paseo Maritimo Benidorm",38.5340,-0.1200),
    (156,"Cap de l Horta Alicante",38.3490,-0.4060),
    (157,"Explanada de Espana",38.3450,-0.4840),
    (158,"Parque El Palmeral Alicante",38.3490,-0.4730),
    (159,"Sierra de Bernia",38.6700,-0.0560),
    (160,"Desert de les Palmes",40.0680,0.0500),
    (161,"Playa Norte Peniscola",40.3710,0.4120),
    (162,"Via Verde Ojos Negros",39.8500,-0.7500),
    (163,"Parque Natural del Montgo",38.7960,0.1600),
    (164,"Platja de l Arenal Javea",38.7590,0.1820),
    (165,"Rio Turia Valencia Sur",39.4690,-0.3830),
    (166,"Font Roja Alcoy",38.6670,-0.5430),
    (167,"Clot de Galvany Elche",38.2510,-0.5110),
    (168,"Palmeral de Elche",38.2660,-0.6960),
    (169,"Sierra de Espadan",39.8790,-0.3550),
    (170,"Playa de Gandia",38.9930,-0.1630),
    (171,"Salinas Torrevieja",37.9780,-0.7020),
    (172,"Greenway Xurra",39.5100,-0.3700),
    (173,"Serra Calderona",39.6530,-0.4200),
    (174,"Parque de Maria Luisa",37.3720,-5.9870),
    (175,"Alamillo Sevilla",37.4120,-5.9970),
    (176,"Canal de Alfonso XIII",37.3630,-6.0020),
    (177,"Muelle de la Sal Triana",37.3830,-6.0020),
    (178,"Paseo Maritimo Malaga",36.7130,-4.4200),
    (179,"Montes de Malaga",36.7650,-4.3800),
    (180,"Desembocadura del Guadalhorce",36.6890,-4.4550),
    (181,"Playa de la Barrosa",36.3810,-6.1910),
    (182,"Paseo Maritimo Cadiz",36.5270,-6.2920),
    (183,"Playa de Cortadura",36.5070,-6.2720),
    (184,"Carrera del Darro Granada",37.1780,-3.5900),
    (185,"Paseo de la Alhambra",37.1770,-3.5870),
    (186,"Sierra Nevada Base",37.0960,-3.3960),
    (187,"Vega de Granada",37.1600,-3.6200),
    (188,"Ribera del Guadalquivir Cordoba",37.8870,-4.7770),
    (189,"Medina Azahara Trail",37.8880,-4.8670),
    (190,"Marismas del Odiel",37.2190,-6.9630),
    (191,"Playa de Matalascanas",36.9880,-6.5650),
    (192,"Parque Natural de Cazorla",37.9130,-2.9240),
    (193,"Cabo de Gata",36.7260,-2.1880),
    (194,"Paseo Maritimo Almeria",36.8360,-2.4550),
    (195,"Paseo Maritimo Estepona",36.4250,-5.1470),
    (196,"Paseo Maritimo Marbella",36.5050,-4.8840),
    (197,"Caminito del Rey",36.9260,-4.7780),
    (198,"Parque de los Alcornocales",36.4260,-5.5900),
    (199,"Sierra de Grazalema",36.7630,-5.3710),
    (200,"Ronda Tajo Trail",36.7420,-5.1650),
    (201,"Parque del Guadalquivir Jaen",37.7660,-3.7860),
    (202,"Playa de Bolonia",36.0880,-5.7740),
    (203,"Punta Espiritu Santo Tarifa",36.0070,-5.6040),
    (204,"Ribera del Genil Granada",37.1690,-3.5990),
    (205,"Dehesa del Generalife",37.1810,-3.5840),
    (206,"Pinares de Cartaya",37.2500,-7.1200),
    (207,"Via Verde de la Sierra",36.9100,-5.4300),
    (208,"Playa de los Lances Tarifa",36.0220,-5.6150),
    (209,"Parque Moret Huelva",37.2620,-6.9580),
    (210,"Desierto de Tabernas",37.0510,-2.3890),
    (211,"Paseo del Parque Malaga",36.7170,-4.4150),
    (212,"Acantilados de Maro",36.7440,-3.8450),
    (213,"Puerto Real Cano Sancti Petri",36.5240,-6.1790),
    (214,"Ribera del Ebro Zaragoza",41.6570,-0.8790),
    (215,"Parque Grande Labordeta",41.6370,-0.8910),
    (216,"Canal Imperial de Aragon",41.6340,-0.9050),
    (217,"Galacho de Juslibol",41.6950,-0.8900),
    (218,"Valle de Ordesa",42.6630,-0.0550),
    (219,"Mallos de Riglos",42.3580,-0.7270),
    (220,"Sendero del Rio Turia Teruel",40.3450,-1.1060),
    (221,"Albarracin Trails",40.4080,-1.4440),
    (222,"Selva de Oza",42.7820,-0.6660),
    (223,"Embalse de Barasona",42.1770,0.3290),
    (224,"Monasterio de Piedra",41.1940,-1.7770),
    (225,"Sierra de Guara",42.2320,-0.0530),
    (226,"Moncayo",41.7840,-1.8370),
    (227,"Camino del Cid Aragon",41.0380,-0.2910),
    (228,"Parque del Agua Zaragoza",41.6850,-0.8570),
    (229,"Senda Ecologica Toledo",39.8580,-4.0260),
    (230,"Ribera del Tajo Toledo",39.8560,-4.0330),
    (231,"Tablas de Daimiel",39.1450,-3.7150),
    (232,"Lagunas de Ruidera",38.9320,-2.8800),
    (233,"Parque Abelardo Sanchez",38.9950,-1.8580),
    (234,"Hoz del Jucar Cuenca",40.0700,-2.1300),
    (235,"Ciudad Encantada Trail",40.2090,-1.9600),
    (236,"Parque de la Concordia Guadalajara",40.6340,-3.1650),
    (237,"Rio Henares Guadalajara",40.6320,-3.1580),
    (238,"Molinos del Guadiana",38.9910,-3.9280),
    (239,"Hayedo de Tejera Negra",41.2380,-3.2620),
    (240,"Parque Nacional de Cabaneros",39.3980,-4.2930),
    (241,"Nacimiento del Rio Mundo",38.4990,-2.4490),
    (242,"Alarcon Embalse",39.6880,-2.0940),
    (243,"Via Verde de la Jara",39.6070,-4.9350),
    (244,"Ribera del Jerte",40.1180,-5.8640),
    (245,"Monfrague",39.8430,-5.9650),
    (246,"Ribera del Guadiana Badajoz",38.8720,-6.9670),
    (247,"Parque del Principe Caceres",39.4760,-6.3730),
    (248,"Embalse de Proserpina",38.9640,-6.3680),
    (249,"Paseo Fluvial Merida",38.9120,-6.3430),
    (250,"Valle del Ambroz",40.2120,-5.8640),
    (251,"Sierra de San Pedro",39.3500,-6.8200),
    (252,"Garganta de los Infiernos",40.1980,-5.7830),
    (253,"Cornalvo",38.9950,-6.2930),
    (254,"Ribera del Segura Murcia",38.0010,-1.1300),
    (255,"Parque de El Valle",37.9600,-1.1250),
    (256,"Calblanque",37.6060,-0.7350),
    (257,"Paseo Maritimo Cartagena",37.5950,-0.9810),
    (258,"Monte de las Cenizas",37.5870,-0.7520),
    (259,"La Manga del Mar Menor",37.6430,-0.7060),
    (260,"Sierra Espuna",37.8630,-1.5620),
    (261,"Salinas de San Pedro",37.8220,-0.8050),
    (262,"Paseo de la Sal Aguilas",37.4050,-1.5810),
    (263,"Rambla del Puerto Mazarron",37.5690,-1.2630),
    (264,"Anaga Tenerife",28.5530,-16.1830),
    (265,"Teide Base Trail",28.2720,-16.6420),
    (266,"Paseo Maritimo Las Americas",28.0560,-16.7290),
    (267,"Barranco del Infierno",28.1080,-16.7270),
    (268,"Dunas de Maspalomas",27.7420,-15.5780),
    (269,"Pico de las Nieves",27.9600,-15.5710),
    (270,"Paseo Maritimo Las Canteras",28.1370,-15.4390),
    (271,"Roque Nublo Circuit",27.9720,-15.6120),
    (272,"Ruta de los Volcanes La Palma",28.5620,-17.8560),
    (273,"Caldera de Taburiente",28.7300,-17.9130),
    (274,"Playa de Famara Lanzarote",29.1040,-13.5580),
    (275,"Ruta de los Volcanes Lanzarote",28.9940,-13.7500),
    (276,"Corralejo Dunes Fuerteventura",28.7270,-13.8660),
    (277,"Garajonay La Gomera",28.1170,-17.2320),
    (278,"Mirador del Rio Trail Lanzarote",29.2130,-13.4800),
    (279,"Paseo Maritimo Palma",39.5660,2.6290),
    (280,"Serra de Tramuntana Soller",39.7660,2.7150),
    (281,"Cala Mondrago",39.3450,3.1890),
    (282,"Cami de Cavalls Menorca",39.9430,3.8230),
    (283,"Cala Macarella Menorca",39.9370,3.9300),
    (284,"Ses Salines Ibiza",38.8670,1.3720),
    (285,"Santa Eularia des Riu",38.9870,1.5350),
    (286,"Cap de Formentor",39.9620,3.1630),
    (287,"Platja de Muro",39.8080,3.1070),
    (288,"Torrent de Pareis",39.8510,2.8230),
    (289,"Paseo Maritimo de Ceuta",35.8920,-5.3130),
    (290,"Monte Hacho",35.8870,-5.2830),
    (291,"Parque Maritimo del Mediterraneo",35.8910,-5.3140),
    (292,"Paseo Maritimo de Melilla",35.2920,-2.9380),
    (293,"Parque de los Pueblos de Espana",35.2880,-2.9510),
    (294,"Rostrogordo",35.2840,-2.9620),
    (295,"Playa de la Concha Algeciras",36.1310,-5.4530),
    (296,"Embalse de El Atazar",40.9060,-3.4750),
    (297,"Paseo Fluvial Avila",40.6530,-4.6990),
    (298,"Playa de las Teresitas Tenerife",28.5090,-16.1880),
    (299,"Parque Natural s Albufera Mallorca",39.7930,3.1060),
    (300,"Senda del Duero Zamora",41.5010,-5.7560),
]


def check_coverage(lat, lng, key):
    url = "https://maps.googleapis.com/maps/api/streetview/metadata"
    r = requests.get(url, params={
        "location": f"{lat},{lng}",
        "source": "outdoor",
        "key": key
    }, timeout=10)
    return r.json().get("status") == "OK"


def download_photo(lat, lng, key, filepath):
    url = "https://maps.googleapis.com/maps/api/streetview"
    r = requests.get(url, params={
        "size": "600x400",
        "location": f"{lat},{lng}",
        "fov": "100",
        "pitch": "0",
        "source": "outdoor",
        "key": key
    }, timeout=15)
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

    for i, (sid, nombre, lat, lng) in enumerate(SPOTS):
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
            ok = download_photo(lat, lng, key, filepath)
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
