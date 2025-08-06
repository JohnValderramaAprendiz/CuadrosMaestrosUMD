import os
import sys

# Agregar el directorio CODIGO al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'CODIGO'))

# Importar la aplicación Flask
from CODIGO.api_backend import app

if __name__ == '__main__':
    # Configuración para Azure App Service
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)