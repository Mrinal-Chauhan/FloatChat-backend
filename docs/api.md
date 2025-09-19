# API Documentation

## FloatChat API

The FloatChat API provides intelligent access to Argo oceanographic float data through an AI-powered chat interface.

### Base URL

```
http://localhost:8000
```

### Endpoints

#### Health Check

**GET /health**

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "FloatChat API",
  "timestamp": "2025-09-20T10:30:00Z"
}
```

#### Root

**GET /**

Returns basic API information.

**Response:**
```json
{
  "status": "FloatChat API is running",
  "version": "1.0.0",
  "timestamp": "2025-09-20T10:30:00Z"
}
```

#### Chat

**POST /api/v1/chat**

Submit a natural language query about Argo data and receive an AI-generated response.

**Request Body:**
```json
{
  "message": "Show me profiles from the Argo-France project in March 2023",
  "session_id": "user123_session456"
}
```

**Response:**
```json
{
  "response": "I found 15 profiles from the Argo-France project in March 2023. Here are the details..."
}
```

**Error Response (422):**
```json
{
  "detail": [
    {
      "loc": ["string", 0],
      "msg": "string", 
      "type": "string"
    }
  ]
}
```

### Query Examples

#### Find profiles by project
```json
{
  "message": "Find profiles from the Argo-France project",
  "session_id": "session_001"
}
```

#### Find profiles by date range
```json
{
  "message": "Show me profiles from March 2023",
  "session_id": "session_002"
}
```

#### Find specific profile
```json
{
  "message": "Get profile for float 5906527 cycle 94",
  "session_id": "session_003"
}
```

#### Geographic queries
```json
{
  "message": "Find profiles near latitude 40, longitude -50",
  "session_id": "session_004"
}
```

### Error Codes

- **200**: Success
- **422**: Validation Error - Invalid request format
- **500**: Internal Server Error - Server-side error

### Rate Limiting

Currently no rate limiting is implemented, but consider implementing rate limiting for production use.