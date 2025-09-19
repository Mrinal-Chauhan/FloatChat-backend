# FloatChat - Intelligent Argo Data Assistant

FloatChat is an AI-powered backend service that provides intelligent access to Argo oceanographic float data through natural language queries. Built for hackathons and professional deployment.

## 🌊 Features

- **Natural Language Queries**: Ask questions about Argo data in plain English
- **AI-Powered Search**: Uses OpenAI GPT models to understand and respond to complex queries
- **MongoDB Integration**: Efficient storage and retrieval of Argo profile data
- **Professional Architecture**: Clean, scalable codebase following enterprise patterns
- **RESTful API**: Well-documented FastAPI endpoints with automatic validation
- **Docker Support**: Containerized for easy deployment

## 🏗️ Project Structure

```
floatchat/
├── app/                    # Main application
│   ├── api/               # FastAPI routes and middleware
│   ├── core/              # Business logic and AI agent
│   ├── database/          # MongoDB operations
│   ├── schemas/           # Pydantic models
│   └── utils/             # Utilities and helpers
├── scripts/               # Data processing scripts
├── data/                  # Argo NetCDF data files
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB (local or cloud)
- OpenAI API key

### Setup

1. **Clone and setup environment:**
   ```bash
   git clone <repo-url>
   cd FloatChat
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and OpenAI API key
   ```

3. **Ingest Argo data:**
   ```bash
   # Place .nc files in data/ directory
   python scripts/ingest_data.py
   ```

4. **Start the server:**
   ```bash
   python main.py
   # or
   uvicorn app.main:app --reload
   ```

5. **Test the API:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "How many Argo profiles do we have?", "session_id": "test"}'
   ```

## 📊 Example Queries

- "Show me profiles from the Argo-France project in March 2023"
- "Find profiles near latitude 40, longitude -50"
- "Get profile for float 5906527 cycle 94"
- "How many profiles do we have from each project?"

## 📡 API Endpoints

### POST /api/v1/chat

Process natural language queries about Argo data.

**Request:**
```json
{
  "message": "Find profiles from the Argo-France project",
  "session_id": "user_session_123"
}
```

**Response:**
```json
{
  "response": "I found 1,245 profiles from the Argo-France project. Here are some details..."
}
```

### GET /health

Health check endpoint.

### Full API documentation available at: `http://localhost:8000/docs`

## 🗄️ Data Schema

Argo profiles are stored in MongoDB with the following structure:

```json
{
  "_id": "5906527_94",
  "float_id": 5906527,
  "cycle_number": 94,
  "time": "2023-03-15T12:00:00Z",
  "project_name": "Argo-France",
  "location": {
    "type": "Point",
    "coordinates": [-40.5, 42.1]
  },
  "measurements": [
    {
      "pressure": 10.5,
      "temperature": 15.2,
      "salinity": 35.1
    }
  ]
}
```

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black app/ scripts/

# Lint code  
flake8 app/ scripts/

# Type checking
mypy app/
```

### Adding New Features

1. **API Endpoints**: Add to `app/api/routes/`
2. **Business Logic**: Add to `app/core/`
3. **Database Operations**: Add to `app/database/`
4. **Data Processing**: Add to `scripts/`

## 🚢 Deployment

### Production Setup

1. **Environment variables:**
   ```bash
   export MONGODB_URI="mongodb://prod-server:27017"
   export OPENAI_API_KEY="your-prod-key"
   export DEBUG=False
   export LOG_LEVEL=WARNING
   ```

2. **Run with Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Using Docker:**
   ```bash
   docker build -t floatchat:latest .
   docker run -p 8000:8000 --env-file .env floatchat:latest
   ```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Setup Guide](docs/setup.md)
- [Deployment Guide](docs/deployment.md)

## 🏆 Architecture Highlights

This project demonstrates professional software engineering practices:

- **Clean Architecture**: Separation of concerns with distinct layers
- **SOLID Principles**: Single responsibility, dependency injection
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive exception handling and logging
- **Testing**: Unit and integration test structure
- **Documentation**: API docs, code comments, and setup guides
- **DevOps**: Docker, docker-compose, environment management
- **Security**: Environment variables, input validation

Perfect for hackathon demonstrations and production deployment!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for the oceanographic research community**