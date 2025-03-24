# Development Environment Setup

Follow these steps to set up the development environment for the FastAPI project.

## 1. Build Postgres & Chroma Databases

Run the following command to build and start the Postgres and Chroma databases using Docker Compose:

```bash
docker compose -f ./deployments/docker-compose.dev.yml --env-file .env.dev up --build -d
```

## 2. Activate Poetry Shell

Activate the Poetry shell by running:

```bash
poetry shell
```

## 3. Install Dependencies

Install the required dependencies using Poetry:

```bash
poetry install
```

## 4. Set Environment Variable

Make sure the following environment variable is defined in all terminal tabs before running any of the following commands:

```bash
export ENV_FILE=".env.dev"
```

To check if the environment variable is set correctly, you can use the following command:

```bash
echo $ENV_FILE
```

## 5. Run Database Migration Scripts

Run the Alembic migration scripts to update the database schema:

```bash
alembic upgrade head
```

## 6. Run the Main Application

Start the main FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

## 7. Run Celery Worker

To process asynchronous tasks, start the Celery worker:

```bash
celery --app=app.celery.celery_app worker -l info
```

## 8. Run Celery Beat for Monitoring Tasks

To monitor the tasks and schedule periodic tasks, run Celery Beat:

```bash
celery --app=app.celery.celery_app flower -l info
```

## 9. Access the API Documentation

Open the following URL in your browser to view the API documentation:

```
localhost:8000/api/docs
```

## 10. Install Make

Make sure `make` is installed on your system.

- **On Linux/macOS**, install using:

  ```bash
  sudo apt install make   # For Debian-based systems
  brew install make       # For macOS
  ```

- **On Windows**, install `make` using Chocolatey:

  ```bash
  choco install make
  ```

### Common Make Commands

```bash
make install   # Install dependencies
make run       # Start FastAPI application
make test      # Run tests
make lint      # Check for linting errors
make format    # Format the code
```

## 11. Install Ruff Plugins and Config File in PyCharm

### 📌 Install Ruff Plugin in PyCharm  
1. Open **PyCharm**.  
2. Navigate to **File** → **Settings** → **Plugins**.  
3. Search for **Ruff** in the marketplace.  
4. Click **Install** and restart PyCharm if necessary.  

### 📌 Config file Ruff Plugin in PyCharm  
1. Open **PyCharm**.  
2. Navigate to **File** → **Settings** → **Tools** → **Ruff**.  
3. Enter file path to Ruff config file **${PROJECT_PATH}/pyproject.toml**.  
4. Click **Apply** and **Ok**. changes.

## 12. Enable File Watcher for Regal OPA
1. Navigate to **File** → **Settings** → **Tools** → **File Watchers**.  
2. Click **+** and select **Custom Watcher**.  
3. Configure as follows:
   - Name: `Regal Linter`
   - File Type: `Rego language file`
   - Scope: `Project Files`
   - Program: `$ProjectFileDir$\app\opa\regal`
   - Arguments: `lint -c "$ProjectFileDir$\app\opa\regal.yml" "$FilePath$"`
   - Working directory: `$ProjectFileDir$`
4. Click **Apply** and **Ok**. changes.
