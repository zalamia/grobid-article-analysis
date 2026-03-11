import unittest
import os

# Test para la práctica de Open Science y AI en RSE
# Hecho para comprobar que he cumplido con los requisitos de las sesiones 2, 3 y 4
class TestMiProyecto(unittest.TestCase):

    # 1. Test para ver si la carpeta con los PDFs está bien
    def test_verificar_pdfs(self):
        # Miramos si existe la carpeta
        self.assertTrue(os.path.exists('pdfs'), 'Uy, no encuentro la carpeta /pdfs')
        
        # Miramos si hay algún PDF dentro (deberían ser 10)
        archivos = os.listdir('pdfs')
        pdfs = [f for f in archivos if f.endswith('.pdf')]
        self.assertGreater(len(pdfs), 0, 'La carpeta pdfs está vacía, mete los artículos')

    # 2. Test para comprobar que no se me ha olvidado ningún archivo de las sesiones
    def test_archivos_principales(self):
        # Archivos que pide el profesor en las diapositivas
        self.assertTrue(os.path.exists('main.py'), 'Falta el script principal main.py')
        self.assertTrue(os.path.exists('Dockerfile'), 'Se te ha olvidado el Dockerfile para la sesión 4')
        self.assertTrue(os.path.exists('requirements.txt'), 'Falta el requirements.txt para que sea reproducible')
        self.assertTrue(os.path.exists('codemeta.json'), 'No encuentro el archivo de metadatos (Sesión 2)')

    # 3. Test para ver si el README tiene la sección de validación (que puntúa mucho)
    def test_contenido_readme(self):
        self.assertTrue(os.path.exists('README.md'), 'El README.md es obligatorio para la entrega')
        
        # Leemos el archivo para ver si hemos explicado la validación
        with open('README.md', 'r', encoding='utf-8') as f:
            texto = f.read()
            # Buscamos la palabra "Validación" en el texto
            encontrado = 'Validación' in texto
            self.assertTrue(encontrado, 'En el README falta explicar cómo has validado los resultados')

if __name__ == '__main__':
    unittest.main()