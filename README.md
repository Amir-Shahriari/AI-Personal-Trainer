
# Personalized Yoga Coach API

This repository contains the backend code for the **Personalized Yoga Coach**, a FastAPI-based application that generates personalized yoga session plans based on user inputs such as session duration, intensity, and target muscle groups. The application uses machine learning models for pose recommendations and plan generation.

---

## Features

- **Personalized Yoga Plans**: Creates yoga sessions tailored to user preferences.
- **Searchable Pose Database**: Uses FAISS for efficient retrieval of yoga poses.
- **Text Generation**: Leverages Hugging Face's GPT-2 for generating additional insights.
- **CORS Support**: Built-in support for Cross-Origin Resource Sharing (CORS).

---

## Project Structure

```plaintext
.
├── main.py               # Backend application code
├── yoga_data.csv         # Yoga pose data
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/personalized-yoga-coach.git
   cd personalized-yoga-coach
   ```

2. **Create a virtual environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Place your data file**:
   Ensure the `yoga_data.csv` file is in the root directory.

---

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   python main.py
   ```

2. **Access the API**:
   Open your browser or a tool like Postman and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. **Interactive API Docs**:
   Visit the automatically generated API documentation:
   ```
   http://127.0.0.1:8000/docs
   ```

---

## API Endpoints

### `GET /`
Welcome message for the API.

### `POST /generate_plan/`
Generates a personalized yoga session plan.

#### Request Body
```json
{
  "duration": 30,             # Total duration in minutes
  "intensity": "medium",      # Intensity level (e.g., low, medium, high)
  "muscles": ["core", "legs"] # List of target muscle groups
}
```

#### Response
```json
{
  "plan": [
    {
      "pose": "Downward Dog",
      "description": "A foundational yoga pose...",
      "duration": "3.0 minutes",
      "instructions": "Place your hands..."
    },
    ...
  ]
}
```

---

## Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)**: A modern web framework for building APIs.
- **[Hugging Face Transformers](https://huggingface.co/transformers/)**: Pretrained models for text generation and embeddings.
- **[FAISS](https://github.com/facebookresearch/faiss)**: Efficient similarity search and clustering.
- **Pandas**: Data manipulation and analysis.
- **UVicorn**: ASGI server for running the FastAPI application.

---

## Deployment

To deploy this application, use platforms like **Heroku**, **AWS**, or **Google Cloud Platform**. Ensure that:
- The `yoga_data.csv` file is included in the deployment.
- Environment variables like `PORT` are correctly configured.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---


## Contact

For questions or feedback, please contact:
**Your Name** - [amirhossein.shahriari@yahoo.com](mailto:amirhossein.shahriari@yahoo.com)
```
