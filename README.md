# Travel Recommendations API

This is a simple FastAPI application that provides travel recommendations for a given country during a specific season. The recommendations are fetched by calling the OpenAI GPT API.

## Features

- Provides travel recommendations based on country and season.
- Caches the recommendations to reduce API calls to OpenAI.
- Includes basic tests to validate functionality and caching behavior.

## Setup

1.  Clone the repository:
    ```
    git clone https://github.com/yourusername/travel-recommendations-api.git
    ```
2.  Setup env:
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    OPENAI_API_KEY=your_openai_api_key
    ```
3.  Run source:
    ### If using docker:
        ```
        docker compose build
        docker compose up -d
        ```
    ### Using Makefile:
        ```
        make local-server
        ```
4.  Make your get request:
    Curl:
    ```
    curl -X 'GET' \
    'http://localhost:3000/recommendations?country=vietnam&season=summer' \
    -H 'accept: application/json'
    ```

```
  Or using swagger UI:
  http://localhost:3000/docs
```
