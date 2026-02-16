# 🛍️ AI Product Recommender API

API RESTful de recomendación de productos y búsqueda semántica construida con **Django REST Framework**, **PostgreSQL (pgvector)** y modelos de **Machine Learning**.

Este proyecto demuestra cómo implementar búsquedas vectoriales para encontrar productos por "significado" y no solo por coincidencia de palabras clave, además de generar recomendaciones de productos similares automáticamente.

## 🚀 Tecnologías

*   **Backend:** Python 3.12, Django 5, Django REST Framework.
*   **Base de Datos:** PostgreSQL 16 con extensión `pgvector`.
*   **AI/ML:** `sentence-transformers` (HuggingFace) para generación de embeddings.
*   **Async:** Celery & Redis para tareas en segundo plano.
*   **CI/CD:** GitHub Actions.

## ✨ Funcionalidades Clave

1.  **Búsqueda Semántica:**
    *   Endpoint: `/api/products/search/?q=algo para jugar`
    *   Entiende el contexto. Buscar "algo para jugar" devolverá "Gaming Mouse" o "Mechanical Keyboard" aunque no contengan la palabra "jugar".

2.  **Recomendaciones (Item-to-Item):**
    *   Endpoint: `/api/products/{id}/recommendations/`
    *   Calcula la distancia del coseno entre vectores para sugerir productos similares.

3.  **Ingesta de Datos Inteligente:**
    *   Script personalizado (`import_amazon_data`) que carga datos crudos y genera embeddings vectoriales al vuelo.

## 🛠️ Instalación y Uso

### Prerrequisitos
*   Python 3.12+
*   PostgreSQL con `pgvector` instalado.
*   Redis (opcional, para Celery).

### Pasos

1.  **Clonar y configurar entorno:**
    ```bash
    https://github.com/Jorgedosaa/product-recommender-api.git
    cd product-recommender-api
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configurar Base de Datos:**
    Asegúrate de tener una DB Postgres corriendo y configura las variables de entorno en un archivo `.env` o exportándolas:
    ```bash
    export DATABASE_URL=postgres://user:pass@localhost:5432/recommender
    ```

3.  **Migraciones e Importación:**
    ```bash
    python manage.py migrate
    # Carga datos de prueba y genera vectores
    python manage.py import_amazon_data
    ```

4.  **Ejecutar Servidor:**
    ```bash
    python manage.py runserver
    ```

## 🧪 Testing

El proyecto cuenta con una suite de tests automatizados (CI/CD integrado).
```bash
python manage.py test products
```