#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  Actualizador automático — Tabla de Tipos Pokémon
#  Hecho por AC - RyLayn · https://github.com/RyLayn
#  Se ejecuta solo (GitHub Actions) y actualiza index.html con
#  el Pokédex más reciente de Pokémon Showdown + hoja de iconos.
#  A prueba de fallos: si algo no valida, NO toca el archivo.
# ============================================================
import json, re, sys, base64, unicodedata, urllib.request

FUENTES_DEX = ["https://play.pokemonshowdown.com/data/pokedex.json",
               "https://cdn.jsdelivr.net/gh/smogon/pokemon-showdown-client@master/play.pokemonshowdown.com/data/pokedex.json"]
FUENTES_IDX = ["https://raw.githubusercontent.com/smogon/pokemon-showdown-client/master/play.pokemonshowdown.com/src/battle-dex-data.ts",
               "https://cdn.jsdelivr.net/gh/smogon/pokemon-showdown-client@master/play.pokemonshowdown.com/src/battle-dex-data.ts"]
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
        filas.append([display(base, forme), ts[0], ts[1] if len(ts) > 1 else "", sid, ico, e['num']])
    vistos, salida = set(), []
    for r in filas:
        if r[0] in vistos: continue
        vistos.add(r[0]); salida.append(r)
    salida.sort(key=lambda x: norm(x[0]))
    return salida

def parse_iconidx(ts):
    start = ts.index('BattlePokemonIconIndexes:')
    end = ts.index('BattlePokemonIconIndexesLeft')
    body = ts[start:end]
    return {k: int(a)+int(b or 0) for k, a, b in re.findall(r"([a-z0-9]+):\s*(\d+)(?:\s*\+\s*(\d+))?\s*,", body)}

def valido(arr, minimo):
    if not isinstance(arr, list) or len(arr) < max(1000, minimo): return False
    for m in arr:
        if not (isinstance(m, list) and len(m) == 6): return False
        if not (isinstance(m[0], str) and 0 < len(m[0]) < 60): return False
        if not (isinstance(m[1], str) and m[1]): return False
        if not isinstance(m[2], str): return False
        if not re.fullmatch(r'[a-z0-9-]+', m[3]): return False
        if not (isinstance(m[4], int) and 0 <= m[4] < 100000): return False
        if not (isinstance(m[5], int) and 0 < m[5] < 100000): return False
    return True

def main():
    html = open('index.html', encoding='utf-8').read()
    m = re.search(r'let MON = (\[\[.*?\]\]);', html, re.S)
    if not m:
        print("::error::no se encontró el dataset en index.html"); return 1
    actual = json.loads(m.group(1))

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

    nuevo = construir(dex, iconidx)
    if not valido(nuevo, len(actual) - 5):  # jamás degradar: no aceptar menos entradas (tolerancia 5)
        print("::error::los datos nuevos no pasaron la validación; index.html queda intacto"); return 1

    nombres_viejos = {x[0] for x in actual}
    novedades = [x[0] for x in nuevo if x[0] not in nombres_viejos]
    cambio_datos = json.dumps(nuevo, ensure_ascii=False, separators=(',',':')) != json.dumps(actual, ensure_ascii=False, separators=(',',':'))

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

    if not cambio_datos and not cambio_sheet:
        print("Sin cambios: todo ya estaba al día. index.html no se toca.")
        return 0

    if cambio_datos:
        html = html[:m.start(1)] + json.dumps(nuevo, ensure_ascii=False, separators=(',',':')) + html[m.end(1):]

    # verificación final antes de escribir (anticorrupción)
    chequeo = re.search(r'let MON = (\[\[.*?\]\]);', html, re.S)
    assert chequeo and valido(json.loads(chequeo.group(1)), 1000), "verificación final falló"
    assert html.count('<script>') == 1 and html.count('</script>') == 1, "estructura dañada"
    assert 'Hecho por AC - RyLayn' in html, "créditos ausentes"

    open('index.html', 'w', encoding='utf-8').write(html)
    print(f"index.html actualizado: {len(nuevo)} entradas"
          + (f" · Novedades ({len(novedades)}): " + ", ".join(novedades[:10]) + ("…" if len(novedades) > 10 else "") if novedades else " · sin Pokémon nuevos")
          + (" · hoja de iconos renovada" if cambio_sheet else ""))
    return 0

if __name__ == "__main__":
    sys.exit(main())
