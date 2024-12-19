# FastAPI Project Setup and Run Guide

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server:**
    ```bash
    cd app
    uvicorn main:app --reload
    ```

2. **Access the API documentation:**
    Open your browser and go to `http://127.0.0.1:8000/docs` for the interactive Swagger UI or `http://127.0.0.1:8000/redoc` for the ReDoc documentation.

## Deployment

For deployment, refer to the FastAPI [deployment guide](https://fastapi.tiangolo.com/deployment/).
