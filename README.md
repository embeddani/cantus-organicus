# Cantus Organicus — GABC → Órgano

Aplicación web que convierte archivos GABC (canto gregoriano) a MIDI y los reproduce como órgano de tubos en el navegador.

## Requisitos

- Python 3.8+
- Los paquetes de `requirements.txt`

## Instalación

```bash
pip install -r requirements.txt
```

## Uso en desarrollo

```bash
python app.py
# Abre http://localhost:5000
```

## Producción

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## Estructura

- `app.py` — Backend Flask
- `gabctk.py` — Conversor GABC→MIDI (de https://github.com/jperon/gabctk)
- `midiutil/` — Librería MIDI (incluida con gabctk)
- `abc2xml/` — Dependencia de gabctk
- `templates/index.html` — Interfaz web con síntesis de órgano
- `uploads/` — Archivos GABC temporales
- `outputs/` — Archivos MIDI generados

## Créditos

- [gabctk](https://github.com/jperon/gabctk) — Conversión GABC→MIDI por jperon
- Síntesis de órgano via Web Audio API + Tone.js
- Inspirado en [virtualbookplayer](https://github.com/barrelorgandiscovery/virtualbookplayer)
