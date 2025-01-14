from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from transformers import pipeline
import faiss
import numpy as np

# Load yoga data
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "yoga_data.csv")
yoga_data = pd.read_csv(file_path)

# Check if required columns exist
required_columns = {"pose", "definition", "intensity", "duration", "instructions", "muscle_groups"}
if not required_columns.issubset(yoga_data.columns):
    raise ValueError(f"The yoga_data.csv file must contain the following columns: {required_columns}")

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Hugging Face sentence transformer model for embeddings
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS Index with the correct dimensionality
sample_embedding_dim = embedding_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(sample_embedding_dim)  # Dynamically set dimension based on the model

# Add yoga data to the FAISS index
def preprocess_and_embed_data(data):
    embeddings = []
    metadata = []
    for i, row in data.iterrows():
        text = f"{row['pose']} {row['definition']} {row['muscle_groups']}"
        embedding = embedding_model.encode(text)
        embeddings.append(embedding)
        metadata.append(row.to_dict())  # Store metadata for retrieval
    embeddings = np.array(embeddings, dtype="float32")
    
    # Add embeddings to the FAISS index
    index.add(embeddings)
    return metadata

metadata = preprocess_and_embed_data(yoga_data)

# Load Hugging Face text-generation model
generator = pipeline("text-generation", model="gpt2")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personalized Yoga Coach"}

@app.post("/generate_plan/")
def generate_plan(duration: int, intensity: str, muscles: list[str]):
    try:
        # Total duration in minutes
        total_duration = duration

        # Maximum duration for each pose (in minutes)
        max_pose_duration = 5

        # Construct a query embedding
        query = f"Intensity: {intensity}. Target muscles: {', '.join(muscles)}."
        query_embedding = embedding_model.encode(query).astype("float32")

        # Search FAISS index for relevant poses
        distances, indices = index.search(np.array([query_embedding]), k=15)  # Retrieve more poses
        retrieved_poses = [metadata[i] for i in indices[0]]

        # Build a structured plan
        plan = []
        used_duration = 0

        for pose in retrieved_poses:
            # Parse the duration range from the CSV
            duration_str = pose["duration"].split("-")[0].strip()  # Take the minimum value of the range
            unit = "seconds" if "second" in duration_str else "minutes"

            # Convert duration to minutes
            if unit == "seconds":
                pose_duration = float(duration_str.split()[0]) / 60
            else:
                pose_duration = float(duration_str.split()[0])  # Already in minutes

            # Limit each pose duration to max_pose_duration
            pose_duration = min(pose_duration, max_pose_duration)

            # Ensure the plan does not exceed the requested duration
            if used_duration + pose_duration > total_duration:
                pose_duration = total_duration - used_duration  # Adjust the last pose duration
                if pose_duration <= 0:
                    break

            plan.append({
                "pose": pose["pose"],
                "description": pose["definition"],
                "duration": f"{pose_duration:.1f} minutes",
                "instructions": pose["instructions"]
            })
            used_duration += pose_duration

            # Stop if we've reached the total duration
            if used_duration >= total_duration:
                break

        # Check if the plan satisfies the requested duration
        if used_duration < total_duration:
            return {
                "message": "Could not fully match the requested duration with available poses.",
                "plan": plan
            }

        return {"plan": plan}

    except Exception as e:
        return {"error": str(e)}





