# AI-Powered Scam Detection API

A FastAPI-based backend system that analyzes audio call transcripts and detects potential scam patterns using multiple scoring mechanisms.

## 🎯 Features

- **Real-time Call Analysis**: Analyzes call transcripts with multiple detection metrics
- **Risk Scoring Algorithm**: Weighted scoring formula combining keyword detection, ML probability, and voice stress analysis
- **Risk Classification**: Categorizes calls as Safe, Suspicious, or Scam
- **Voice Alerts**: Generates appropriate warning messages based on risk level
- **Input Validation**: Pydantic models ensure data integrity
- **RESTful API**: Clean, documented API endpoints

## 📊 Risk Scoring Formula

```
Final Risk Score = (Keyword Score × 0.4) + (ML Probability × 0.5) + (Voice Stress Score × 0.1)
```

### Risk Categories

| Score Range | Risk Label | Alert Message |
|-------------|------------|---------------|
| 0-30 | Safe | "This call appears safe." |
| 31-70 | Suspicious | "Warning. This call shows suspicious scam patterns." |
| 71-100 | Scam | "Danger! This call is highly likely to be a scam." |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

4. **View API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### POST /analyze-call

Analyzes a call and returns risk assessment.

**Request Body:**
```json
{
  "transcript": "Your call transcript here",
  "keyword_score": 45.5,
  "ml_probability": 60.0,
  "voice_stress_score": 30.0
}
```

**Response:**
```json
{
  "final_risk_score": 51.5,
  "risk_label": "Suspicious",
  "transcript": "Your call transcript here",
  "detected_keywords_score": 45.5,
  "ml_scam_probability": 60.0,
  "voice_stress_score": 30.0,
  "voice_alert_message": "Warning. This call shows suspicious scam patterns."
}
```

**Field Constraints:**
- `transcript`: Non-empty string
- `keyword_score`: Float between 0-100
- `ml_probability`: Float between 0-100
- `voice_stress_score`: Float between 0-100

### GET /

Root endpoint to verify API status.

### GET /health

Health check endpoint for monitoring.

## 🧪 Testing

Run the test suite to see sample scenarios:

```bash
python test_api.py
```

**Test Cases Include:**
- Safe call (low risk score)
- Suspicious call (medium risk score)
- Scam call (high risk score)
- Boundary value testing

### Manual Testing with curl

**Safe Call Example:**
```bash
curl -X POST "http://localhost:8000/analyze-call" \
  -H "Content-Type: application/json" \
  -d "{\"transcript\": \"Hello, legitimate customer service call\", \"keyword_score\": 10, \"ml_probability\": 15, \"voice_stress_score\": 5}"
```

**Scam Call Example:**
```bash
curl -X POST "http://localhost:8000/analyze-call" \
  -H "Content-Type: application/json" \
  -d "{\"transcript\": \"URGENT! Send money now!\", \"keyword_score\": 85, \"ml_probability\": 95, \"voice_stress_score\": 90}"
```

## 📁 Project Structure

```
AI-powered-audio-call-analyzer/
├── main.py              # Main FastAPI application
├── test_api.py          # Test suite with sample cases
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

The API runs on `0.0.0.0:8000` by default. To change the port or host:

```python
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 📝 Code Structure

### Main Components

1. **Pydantic Models**
   - `CallAnalysisRequest`: Validates incoming requests
   - `CallAnalysisResponse`: Structures API responses

2. **Risk Scoring Functions**
   - `calculate_risk_score()`: Applies weighted formula
   - `determine_risk_label()`: Categorizes risk level
   - `generate_voice_alert()`: Creates alert messages

3. **API Endpoints**
   - `/analyze-call`: Main analysis endpoint
   - `/`: Status check
   - `/health`: Health monitoring

## 🛡️ Error Handling

The API includes comprehensive error handling:
- Input validation via Pydantic
- Empty transcript detection
- Score range validation (0-100)
- Exception handling with appropriate HTTP status codes

## 📚 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations

## 🎓 Example Use Cases

1. **Real-time Call Monitoring**: Analyze ongoing calls for scam detection
2. **Post-call Analysis**: Review recorded call transcripts
3. **Training Data Collection**: Gather labeled data for ML model improvement
4. **Customer Protection**: Alert users about potential scam calls

## 📈 Future Enhancements

- Database integration for call history
- Authentication and authorization
- Batch processing for multiple calls
- Advanced ML model integration
- Real-time websocket support
- Detailed analytics dashboard

## 📄 License

This project is part of the HCL GUVI 2026 Hackathon.

## 🤝 Contributing

Contributions are welcome! Please ensure all tests pass before submitting pull requests.

---

**Built with FastAPI** | **Python 3.8+** | **HCL GUVI Hackathon 2026**