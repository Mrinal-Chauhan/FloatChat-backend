# Setup Instructions

## Prerequisites

- Python 3.11 or higher
- MongoDB instance (local or cloud)
- OpenAI API key

## Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd FloatChat
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=your_mongodb_connection_string_here
   DB_NAME=argo_data
   COLLECTION_NAME=profiles
   DEBUG=True
   LOG_LEVEL=INFO
   ```

## Database Setup

### Option 1: Using MongoDB Atlas (Cloud)

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Get the connection string and update `MONGODB_URI` in `.env`

### Option 2: Using Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service
3. Update `MONGODB_URI=mongodb://localhost:27017` in `.env`

### Option 3: Using Docker

```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

## Data Ingestion

1. **Place NetCDF files in the `data/` directory**

2. **Run the ingestion script:**
   ```bash
   python scripts/ingest_data.py
   ```

3. **Verify data ingestion:**
   Check MongoDB for the ingested profiles in your specified database and collection.

## Running the Application

### Development Mode

```bash
python -m app.main
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t floatchat .
docker run -p 8000:8000 --env-file .env floatchat
```

## Verification

1. **Check API health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "How many profiles do we have?",
       "session_id": "test_session"
     }'
   ```

3. **View API documentation:**
   Open `http://localhost:8000/docs` in your browser

## Data Analysis Scripts

### Analyze NetCDF files
```bash
python scripts/analyze_netcdf.py
```

### Custom data processing
```bash
# Add your custom scripts to scripts/ directory
python scripts/your_custom_script.py
```

## Troubleshooting

### Common Issues

1. **MongoDB connection failed:**
   - Check `MONGODB_URI` in `.env`
   - Ensure MongoDB is running
   - Check firewall settings

2. **OpenAI API errors:**
   - Verify `OPENAI_API_KEY` in `.env`
   - Check API quota and billing

3. **Import errors:**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

4. **Port already in use:**
   - Change port in startup command: `--port 8001`
   - Or kill process using the port

### Logs

Check application logs for detailed error information:
- Development: Logs printed to console
- Production: Configure log files in `app/utils/logging.py`