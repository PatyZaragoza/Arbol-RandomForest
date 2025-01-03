# Patricia Zaragoza Palma 
# ingeniería en sistemas computacionales 

from flask import Flask, render_template
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import Preprocessor
import os

app = Flask(__name__)

# Rutas de los archivos Notebook
NOTEBOOKS = [
    {
        "name": "Random Forest",
        "path": "/home/paty/Documentos/septimo7/Programacion_logica/RandomForest.ipynb"
    },
    {
        "name": "Árboles",
        "path": "/home/paty/Documentos/septimo7/Programacion_logica/Forest/Arboles.ipynb"
    },
]

class CleanNotebookPreprocessor(Preprocessor):
    """
    Preprocesador para limpiar notebooks:
    - Elimina celdas vacías.
    - Elimina el código en celdas de tipo código.
    """
    def preprocess(self, notebook, resources):
        cleaned_cells = []
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                if cell['outputs']:
                    # Ocultar el código pero conservar las salidas
                    cell['source'] = ''
                    cleaned_cells.append(cell)
            elif cell.cell_type in ['markdown', 'raw']:
                # Conservar celdas markdown y raw si no están vacías
                if cell['source'].strip():
                    cleaned_cells.append(cell)
        notebook.cells = cleaned_cells
        return notebook, resources


def convert_notebook_to_html(notebook_path):
    """
    Convierte un archivo .ipynb a HTML sin celdas vacías ni código.
    """
    with open(notebook_path) as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    # Configurar el exportador con el preprocesador personalizado
    html_exporter = HTMLExporter()
    html_exporter.register_preprocessor(CleanNotebookPreprocessor, enabled=True)

    # Convertir el notebook
    body, _ = html_exporter.from_notebook_node(notebook_content)
    return body

@app.route('/')
def index():
    notebook_contents = []

    for notebook in NOTEBOOKS:
        html_content = convert_notebook_to_html(notebook["path"])
        notebook_contents.append({
            "name": notebook["name"],
            "content": html_content
        })

    return render_template('index.html', notebooks=notebook_contents)

if __name__ == '__main__':
    app.run(debug=True)
