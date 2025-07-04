# Translation Service

**Translation Service** is a microservice within the **KeenOn Card Generate** project. It handles the translation of text into Chinese for use in learning cards.

## Overview

The Translation Service focuses on processing input text and returning translated content suitable for educational use. It integrates seamlessly with the **Central Hub API** via **gRPC**, ensuring efficient communication and data exchange.

## Key Features
- **Language Translation**: Converts English text into Chinese characters.
- **Educational Focus**: Tailored translations for language learners.
- **gRPC Integration**: Allows smooth and reliable service communication.
- **Python Implementation**: Showcases backend capabilities using Python.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)
- Access to translation APIs (if applicable)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/orchestrator-repo.git
   cd orchestrator-repo/services/keenOn-card-translate
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the sample environment file
   cp sample.env .env
   # Edit .env with your configuration
   ```

5. Start the service:
   ```bash
   # With Docker (recommended)
   docker-compose up -d

   # Without Docker
   python src/main.py
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

## Development Workflow

1. Make changes to the codebase
2. Run linting:
   ```bash
   flake8 src
   ```
3. Run tests:
   ```bash
   pytest
   ```
4. Format code:
   ```bash
   black src
   ```

## Deployment

### Production Deployment

```bash
# Build the Docker image
docker build -t keenon-card-translate:latest .

# Run with Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
```

## API Documentation

The service exposes gRPC endpoints defined in the `proto` directory. The main service methods include:

- `TranslateText`: Translates text from English to Chinese
- `GetCharacterBreakdown`: Provides detailed information about Chinese characters
- `GetExampleSentences`: Returns example sentences using the translated text

## Technologies Used
- **Python**: Primary programming language for the service.
- **gRPC**: Protocol for communicating with the central API.
- **Docker**: Containerized for deployment consistency.
- **pytest**: Testing framework.
- **flake8/black**: Code quality and formatting tools.

---

> **Note:** This project is not production-ready but is intended as a demonstration of my learning progress in backend development.
