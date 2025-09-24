Backend de ejemplo en Python (FastAPI) para un CRUD de tareas.

Requisitos
- Python 3.8+

Instalación y prueba rápida (macOS / zsh)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ejecutar test de humo (crea, consulta, actualiza, borra)
python -m app.smoke_test
# o arrancar la API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints principales
- POST /tasks  -> crear
- GET  /tasks  -> listar
- GET  /tasks/{id} -> leer
- PUT  /tasks/{id} -> actualizar
- DELETE /tasks/{id} -> borrar

Base de datos: SQLite local `tasks.db` en la carpeta `backend/`.
