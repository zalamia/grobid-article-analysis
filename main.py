# ==========================================================
# TRABAJO INDIVIDUAL: Análisis de artículos con Grobid
# Alumno: Bouchra Zalamia
# Asignatura: Open Science y AI en Research Software Engineering
# ==========================================================

import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configuración de Grobid (suponiendo que corre en el puerto por defecto)
URL_GROBID = "http://localhost:8070/api/processFulltextDocument"
CARPETA_ENTRADA = "pdfs"
ARCHIVO_LINKS = "enlaces_extraidos.txt"

def procesar_articulos():
    # Primero miramos si la carpeta con los 10 pdfs existe
    if not os.path.exists(CARPETA_ENTRADA):
        print(f"Error: No encuentro la carpeta '{CARPETA_ENTRADA}'.")
        return

    # Cogemos todos los archivos .pdf de la carpeta
    lista_pdfs = sorted([f for f in os.listdir(CARPETA_ENTRADA) if f.endswith('.pdf')])
    
    todos_los_abstracts = []
    conteo_figuras = {}
    
    # Preparamos el fichero de texto para guardar los enlaces (Requisito 3)
    with open(ARCHIVO_LINKS, "w", encoding="utf-8") as f_txt:
        f_txt.write("LISTA DE ENLACES ENCONTRADOS EN LOS PAPERS\n")
        f_txt.write("==========================================\n\n")

    print(f"Empezando a procesar {len(lista_pdfs)} archivos con Grobid...")

    for nombre_archivo in lista_pdfs:
        ruta_completa = os.path.join(CARPETA_ENTRADA, nombre_archivo)
        
        try:
            # Enviamos el PDF a la API de Grobid
            with open(ruta_completa, 'rb') as pdf_file:
                respuesta = requests.post(URL_GROBID, files={'input': pdf_file})
            
            if respuesta.status_code != 200:
                print(f"Fallo al procesar {nombre_archivo}")
                continue

            # Parseamos el XML que nos devuelve Grobid
            soup = BeautifulSoup(respuesta.text, 'xml')
            
            # --- 1. Extraer el Abstract (para la nube de palabras) ---
            tag_abstract = soup.find('abstract')
            if tag_abstract:
                todos_los_abstracts.append(tag_abstract.get_text())
            
            # --- 2. Contar las figuras (para el gráfico de barras) ---
            todas_las_figuras = soup.find_all('figure')
            conteo_figuras[nombre_archivo] = len(todas_las_figuras)
            
            # --- 3. Extraer los links (Requisito 3 de la práctica) ---
            links_del_paper = []
            # Buscamos etiquetas ptr o ref que tengan un atributo 'target'
            for etiqueta in soup.find_all(['ptr', 'ref']):
                url = etiqueta.get('target')
                if url and url.startswith('http'):
                    links_del_paper.append(url)
            
            # Guardamos los links únicos en nuestro archivo de texto
            with open(ARCHIVO_LINKS, "a", encoding="utf-8") as f_txt:
                f_txt.write(f"Artículo: {nombre_archivo}\n")
                # Usamos set() para no repetir el mismo link si sale varias veces
                for link in set(links_del_paper):
                    f_txt.write(f"  - {link}\n")
                f_txt.write("\n")

            print(f"Procesado correctamente: {nombre_archivo}")

        except Exception as e:
            print(f"Error con el archivo {nombre_archivo}: {e}")

    # --- Generación de Visualizaciones ---

    # Creamos la nube de palabras si tenemos abstracts
    if todos_los_abstracts:
        print("Generando nube de palabras...")
        texto_unido = " ".join(todos_los_abstracts)
        nube = WordCloud(width=800, height=400, background_color='white').generate(texto_unido)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(nube, interpolation='bilinear')
        plt.axis('off')
        plt.title("Palabras más usadas en los Abstracts")
        plt.savefig("nube_palabras.png")
        plt.close() # Cerramos para no gastar memoria

    # Creamos el gráfico de barras para las figuras
    if conteo_figuras:
        print("Generando gráfico de barras...")
        nombres = list(conteo_figuras.keys())
        valores = list(conteo_figuras.values())
        
        plt.figure(figsize=(12, 6))
        plt.bar(nombres, valores, color='skyblue')
        plt.xlabel('Nombre del Artículo')
        plt.ylabel('Cantidad de Figuras')
        plt.title('Figuras encontradas por cada PDF')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("grafico_figuras.png")
        plt.close()

    print("\n¡Todo listo!")
    print(f"Resultados guardados en: 'nube_palabras.png', 'grafico_figuras.png' y '{ARCHIVO_LINKS}'")

if __name__ == "__main__":
    procesar_articulos()