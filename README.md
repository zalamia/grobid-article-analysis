# Análisis de Artículos Científicos con Grobid

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)

Este proyecto automatiza el análisis de 10 artículos de investigación usando **Grobid**.

## Método 1: Instalación con Docker (Recomendado)
Para garantizar la reproducibilidad (Sesión 4):
1. Servidor Grobid: `docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.2`
2. Construir imagen: `docker build -t mi-practica-ai .`
3. Ejecutar: `docker run --rm --network="host" -v ${PWD}:/app mi-practica-ai`

## Método 2: Instalación Local
1. `python -m venv env`
2. `.\env\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python main.py`

## Validación de Resultados
- **Figuras:** Se validó manualmente el `paper1.pdf` (29 figuras), coincidiendo con el script.
- **Enlaces:** El archivo `enlaces_extraidos.txt` contiene URLs reales y verificadas.
- **Abstracts:** La nube de palabras coincide con la temática de IA de los papers.

## Limitaciones
- Requiere conexión al puerto 8070.
- Solo procesa archivos con extensión `.pdf`.

## Metadatos y Licencia
- Ver metadatos en `codemeta.json`.
- Licencia: **CC BY-NC-SA 4.0**.

---
*Realizado por Bouchra Zalamia para la asignatura RSE.*