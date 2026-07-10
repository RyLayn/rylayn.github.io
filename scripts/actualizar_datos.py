#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  Actualizador automático — Tabla de Tipos Pokémon
#  Hecho por AC - RyLayn · https://github.com/RyLayn
#  Se ejecuta solo (GitHub Actions) y actualiza index.html con:
#  Pokédex + stats base + movimientos (España/Latino) + iconos.
#  A prueba de fallos: si algo no valida, NO toca el archivo.
# ============================================================
import json, re, sys, base64, unicodedata, urllib.request

FUENTES_DEX = ["https://play.pokemonshowdown.com/data/pokedex.json",
               "https://cdn.jsdelivr.net/gh/smogon/pokemon-showdown-client@master/play.pokemonshowdown.com/data/pokedex.json"]
FUENTES_IDX = ["https://raw.githubusercontent.com/smogon/pokemon-showdown-client/master/play.pokemonshowdown.com/src/battle-dex-data.ts",
               "https://cdn.jsdelivr.net/gh/smogon/pokemon-showdown-client@master/play.pokemonshowdown.com/src/battle-dex-data.ts"]
FUENTES_MOV = ["https://play.pokemonshowdown.com/data/moves.json",
               "https://cdn.jsdelivr.net/gh/smogon/pokemon-showdown-client@master/play.pokemonshowdown.com/data/moves.json"]
FUENTES_PKM = ["https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/moves.csv",
               "https://cdn.jsdelivr.net/gh/PokeAPI/pokeapi@master/data/v2/csv/moves.csv"]
FUENTES_PKN = ["https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/move_names.csv",
               "https://cdn.jsdelivr.net/gh/PokeAPI/pokeapi@master/data/v2/csv/move_names.csv"]
FUENTE_SHEET = "https://play.pokemonshowdown.com/sprites/pokemonicons-sheet.png"

EN2ES = {"Normal":"Normal","Fighting":"Pelea","Flying":"Volador","Poison":"Veneno","Ground":"Tierra",
"Rock":"Roca","Bug":"Insecto","Ghost":"Fantasma","Steel":"Acero","Fire":"Fuego","Water":"Agua",
"Grass":"Planta","Electric":"Eléctrico","Psychic":"Psíquico","Ice":"Hielo","Dragon":"Dragón","Dark":"Siniestro","Fairy":"Hada"}

def bajar(urls, binario=False):
    ultimo = None
    for u in (urls if isinstance(urls, list) else [urls]):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (TablaTiposPokemon-RyLayn)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return data if binario else data.decode("utf-8")
        except Exception as e:
            ultimo = e
    raise ultimo or RuntimeError("sin respuesta")

toid = lambda x: re.sub(r'[^a-z0-9]', '', x.lower())
def norm(x): return unicodedata.normalize('NFD', x).encode('ascii','ignore').decode().lower()

def display(base, forme):
    if not forme: return base
    m = re.fullmatch(r'Mega(?:-([XYZ]))?', forme)
    if m: return f"Mega {base}" + (f" {m.group(1)}" if m.group(1) else "")
    for tag, lab in [("Alola","de Alola"), ("Galar","de Galar"), ("Hisui","de Hisui")]:
        if forme == tag: return f"{base} {lab}"
        if forme.startswith(tag+"-"): return f"{base} {lab} ({forme[len(tag)+1:]})"
    if forme.startswith("Paldea"):
        rest = forme[7:] if len(forme) > 6 else ""
        return f"{base} de Paldea" + (f" ({rest})" if rest else "")
    return f"{base} ({forme})"

def construir(dex, iconidx):
    base_types = {e['name']: e['types'] for e in dex.values() if e.get('num',0) > 0 and 'forme' not in e}
    filas = []
    for e in dex.values():
        if e.get('num',0) <= 0: continue
        forme = e.get('forme','')
        if forme and re.search(r'Totem|Gmax', forme): continue
        base = e.get('baseSpecies', e['name'])
        keep = (not forme) or re.match(r'Mega|Alola|Galar|Hisui|Paldea', forme) or (e['types'] != base_types.get(base, e['types']))
        if not keep: continue
        ts = [EN2ES.get(t, t) for t in e['types']]
        sid = toid(base) + (('-'+toid(forme)) if forme else '')
        ico = iconidx.get(sid.replace('-',''), e['num'])
        bs = e['baseStats']
        stats = [bs['hp'], bs['atk'], bs['def'], bs['spa'], bs['spd'], bs['spe']]
        filas.append([display(base, forme), ts[0], ts[1] if len(ts) > 1 else "", sid, ico, e['num'], stats])
    vistos, salida = set(), []
    for r in filas:
        if r[0] in vistos: continue
        vistos.add(r[0]); salida.append(r)
    salida.sort(key=lambda x: norm(x[0]))
    return salida

def construir_movs(mvj, moves_csv, names_csv):
    pkid = {}
    for line in moves_csv.split("\n")[1:]:
        c = line.split(",")
        if len(c) < 2: continue
        pkid[toid(c[1])] = int(c[0])
    es, la = {}, {}
    for line in names_csv.split("\n")[1:]:
        i1 = line.find(","); i2 = line.find(",", i1+1)
        if i2 < 0: continue
        mid = int(line[:i1]); lang = line[i1+1:i2]; name = line[i2+1:].rstrip("\r")
        if lang == "7": es[mid] = name
        elif lang == "14": la[mid] = name
    filas = []
    for e in mvj.values():
        if e.get('num',0) <= 0: continue
        if e.get('category') == "Status": continue
        if e.get('isNonstandard') in ("CAP","Custom"): continue
        if e.get('isMax') or e.get('isZ'): continue
        mid = pkid.get(toid(e['name']))
        nla = la.get(mid) if mid else None
        nes = es.get(mid) if mid else None
        if not nla and not nes:
            nla = e['name']; nes = e['name']
        elif not nla: nla = nes
        elif not nes: nes = nla
        bp = e.get('basePower', 0) or 0
        cat = 1 if e.get('category') == "Special" else 0
        filas.append([nla, nes if nes != nla else "", EN2ES.get(e['type'], e['type']), toid(e['name']), bp, cat])
    filas.sort(key=lambda x: norm(x[0]))
    return filas

def parse_iconidx(ts):
    start = ts.index('BattlePokemonIconIndexes:')
    end = ts.index('BattlePokemonIconIndexesLeft')
    body = ts[start:end]
    return {k: int(a)+int(b or 0) for k, a, b in re.findall(r"([a-z0-9]+):\s*(\d+)(?:\s*\+\s*(\d+))?\s*,", body)}

def valido(arr, minimo):
    if not isinstance(arr, list) or len(arr) < max(1000, minimo): return False
    for m in arr:
        if not (isinstance(m, list) and len(m) == 7): return False
        if not (isinstance(m[0], str) and 0 < len(m[0]) < 60): return False
        if not (isinstance(m[1], str) and m[1]): return False
        if not isinstance(m[2], str): return False
        if not re.fullmatch(r'[a-z0-9-]+', m[3]): return False
        if not (isinstance(m[4], int) and 0 <= m[4] < 100000): return False
        if not (isinstance(m[5], int) and 0 < m[5] < 100000): return False
        if not (isinstance(m[6], list) and len(m[6]) == 6 and all(isinstance(v,int) and 0 < v <= 260 for v in m[6])): return False
    return True

def valido_movs(arr, minimo):
    if not isinstance(arr, list) or len(arr) < max(500, minimo): return False
    for m in arr:
        if not (isinstance(m, list) and len(m) == 6): return False
        if not (isinstance(m[0], str) and 0 < len(m[0]) < 45): return False
        if not (isinstance(m[1], str) and len(m[1]) < 45): return False
        if not (isinstance(m[2], str) and m[2]): return False
        if not re.fullmatch(r'[a-z0-9]+', m[3]): return False
        if not (isinstance(m[4], int) and 0 <= m[4] <= 300): return False
        if m[5] not in (0, 1): return False
    return True

def main():
    html = open('index.html', encoding='utf-8').read()
    m = re.search(r'let MON = (\[\[.*?\]\]);', html, re.S)
    mm = re.search(r'let MOV = (\[\[.*?\]\]);', html, re.S)
    if not m or not mm:
        print("::error::no se encontraron los datasets en index.html"); return 1
    actual = json.loads(m.group(1))
    actual_mov = json.loads(mm.group(1))

    print("Descargando Pokédex de Showdown…")
    dex = json.loads(bajar(FUENTES_DEX))
    print(f"  {len(dex)} registros")
    print("Descargando índices de iconos…")
    try:
        iconidx = parse_iconidx(bajar(FUENTES_IDX))
        print(f"  {len(iconidx)} índices de formas")
    except Exception as e:
        print(f"  aviso: sin índices ({e}); se usarán números de dex")
        iconidx = {}
    print("Descargando movimientos + nombres España/Latino…")
    nuevo_mov = None
    try:
        mvj = json.loads(bajar(FUENTES_MOV))
        nuevo_mov = construir_movs(mvj, bajar(FUENTES_PKM), bajar(FUENTES_PKN))
        print(f"  {len(nuevo_mov)} movimientos de daño")
    except Exception as e:
        print(f"  aviso: movimientos no actualizados ({e})")

    nuevo = construir(dex, iconidx)
    if not valido(nuevo, len(actual) - 5):
        print("::error::los datos nuevos no pasaron la validación; index.html queda intacto"); return 1
    if nuevo_mov is not None and not valido_movs(nuevo_mov, len(actual_mov) - 5):
        print("  aviso: los movimientos no pasaron la validación; se conservan los actuales")
        nuevo_mov = None

    dumps = lambda x: json.dumps(x, ensure_ascii=False, separators=(',',':'))
    nombres_viejos = {x[0] for x in actual}
    novedades = [x[0] for x in nuevo if x[0] not in nombres_viejos]
    cambio_datos = dumps(nuevo) != dumps(actual)
    cambio_movs = nuevo_mov is not None and dumps(nuevo_mov) != dumps(actual_mov)

    cambio_sheet = False
    try:
        print("Descargando hoja de iconos…")
        png = bajar(FUENTE_SHEET, binario=True)
        if png[:4] == b'\x89PNG' and 100_000 < len(png) < 3_000_000:
            b64 = base64.b64encode(png).decode()
            patron = r'(--sheet:url\(data:image/png;base64,)[A-Za-z0-9+/=]+(\))'
            if re.search(patron, html):
                nuevo_html = re.sub(patron, r'\g<1>' + b64 + r'\g<2>', html, count=1)
                if nuevo_html != html:
                    html = nuevo_html; cambio_sheet = True
                    print(f"  hoja actualizada ({len(png)//1024} KB)")
        else:
            print("  hoja descartada: no es un PNG válido")
    except Exception as e:
        print(f"  aviso: hoja no actualizada ({e})")

    if not cambio_datos and not cambio_movs and not cambio_sheet:
        print("Sin cambios: todo ya estaba al día. index.html no se toca.")
        return 0

    # aplicar parches (recalculando posiciones tras cada cambio)
    if cambio_datos:
        m = re.search(r'let MON = (\[\[.*?\]\]);', html, re.S)
        html = html[:m.start(1)] + dumps(nuevo) + html[m.end(1):]
    if cambio_movs:
        mm = re.search(r'let MOV = (\[\[.*?\]\]);', html, re.S)
        html = html[:mm.start(1)] + dumps(nuevo_mov) + html[mm.end(1):]

    # verificación final antes de escribir (anticorrupción)
    chequeo = re.search(r'let MON = (\[\[.*?\]\]);', html, re.S)
    assert chequeo and valido(json.loads(chequeo.group(1)), 1000), "verificación final MON falló"
    chequeo2 = re.search(r'let MOV = (\[\[.*?\]\]);', html, re.S)
    assert chequeo2 and valido_movs(json.loads(chequeo2.group(1)), 500), "verificación final MOV falló"
    assert html.count('<script>') == 2 and html.count('</script>') == 2, "estructura dañada"
    assert 'Hecho por AC - RyLayn' in html, "créditos ausentes"

    open('index.html', 'w', encoding='utf-8').write(html)
    movs_nuevos = (len(nuevo_mov) - len(actual_mov)) if cambio_movs else 0
    print(f"index.html actualizado: {len(nuevo)} Pokémon · {len(nuevo_mov) if nuevo_mov else len(actual_mov)} movimientos"
          + (f" · Novedades ({len(novedades)}): " + ", ".join(novedades[:10]) + ("…" if len(novedades) > 10 else "") if novedades else "")
          + (f" · {movs_nuevos} movimientos nuevos" if movs_nuevos > 0 else "")
          + (" · hoja de iconos renovada" if cambio_sheet else ""))
    return 0

if __name__ == "__main__":
    sys.exit(main())
