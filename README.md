# NFL Stats XML Web Service

A SOAP/XML web service that provides NFL player statistics and generates radar charts for player comparisons.

## Project Overview
- SOAP/XML web service for NFL player statistics
- Radar chart visualization for player comparisons
- Modern web UI for data interaction
- Integration with existing NFL stats database

## Project Structure
```
nfl-stats-xml/
├── src/
│   ├── soap_service/      # SOAP service implementation
│   ├── schemas/           # XML schemas and WSDL definitions
│   ├── web_ui/           # Frontend application
│   └── database/         # Database connection (read-only)
├── tests/                # Unit and integration tests
└── docs/                # API documentation
```

## Technical Stack
- Backend:
  - Python with spyne for SOAP service
  - lxml for XML processing
  - xmlschema for validation
  - PostgreSQL (read-only connection)
- Frontend:
  - React for web interface
  - D3.js for radar charts
  - XML/XSLT for data transformation

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

## Development
- Run tests: `pytest`
- Start development server: `python src/soap_service/main.py`
- Access WSDL at: `http://localhost:8000/?wsdl`

## License
MIT 