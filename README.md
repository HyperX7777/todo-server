# FastAPI Todo App

This is a FastAPI application for managing todo items.

## Features

- **Create Todo**: Allows users to create a new todo item.
- **Get All Todos**: Retrieves all todo items from the database.
- **Greet User**: A simple endpoint to greet the user.

## Setup

### Prerequisites

- Python 3.7+
- Poetry
- PostgreSQL Database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/todo-app.git
   ```
### Install Dependencies

   ```bash
poetry install
   ```

 Set up the database URL in .env

## Run the FastAPI server:

   ```bash
    poetry run uvicorn app.main:todo_server --reload
   ```

## Usage

- Create Todo: Send a POST request to /todo endpoint with a JSON body containing the todo title.
- Get All Todos: Send a GET request to /todo endpoint.
- Greet User: Send a GET request to the root / endpoint.

## API Documentation

API documentation is automatically generated by FastAPI and can be viewed by visiting **http://localhost:8000/docs**.
