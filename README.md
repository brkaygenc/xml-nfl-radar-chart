# NFL Stats Radar Chart

A web application that visualizes NFL player statistics using interactive radar charts. Compare up to 5 players in the same position to analyze their performance across different metrics.

## Features

- Search players by name and position
- Compare up to 5 players simultaneously
- Interactive radar chart visualization
- Position-specific statistics
- Modern, responsive UI
- Real-time updates

## Live Demo

The application is deployed on Heroku:
[NFL Stats Radar Chart](https://nfl-stats-radar-charts-7697747f5467.herokuapp.com/)

## Tech Stack

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript (D3.js)
- Database: PostgreSQL
- Deployment: Heroku

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/brkaygenc/xml-nfl-radar-chart.git
cd xml-nfl-radar-chart
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd src
python -m uvicorn soap_service.main:app --reload
```

4. Open http://localhost:8000 in your browser

## License

MIT License 