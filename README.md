
# In-Car AI Assistant

[![Live Demo](https://img.shields.io/badge/Live_Demo-Frontend-brightgreen?style=for-the-badge&logo=vercel)](https://car-ai-assistant-one.vercel.app)
[![Backend API](https://img.shields.io/badge/Backend_API-Live-blue?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/Vishalchand0808/car-ai-backend)

A full-stack, AI-powered conversational assistant designed for an in-car experience. This application understands natural language commands to play music based on mood, fetch real-time weather, and simulate in-car functions like navigation, climate control, and calling.



## Core Features

-   **Natural Language Understanding (NLU):** The assistant accurately classifies user commands into one of five core intents.
-   **Intelligent Entity Extraction:** It identifies and extracts key details from commands, such as locations, artist names, contact names, languages, and user moods.
-   **Mood-Based Music:** Leverages the Spotify API to find and play music that matches the user's detected mood or specific requests.
-   **Real-time Weather:** Integrates with the OpenWeatherMap API to provide current weather conditions for any specified location.
-   **Simulated In-Car Functions:** Demonstrates the ability to handle commands for navigation, climate control, and hands-free calling.
-   **Full-Stack Architecture:** A complete application with a separate React frontend and a Python (FastAPI) backend.

---
## Architecture & Tech Stack

This project is built with a modern, decoupled architecture, where the frontend UI is separate from the backend logic and the core AI model is deployed as its own microservice.



| Category      | Technology                                                                                                                                                              |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white) |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-27A494?style=for-the-badge)                                                              |
| **AI / ML** | ![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-FFD21E?style=for-the-badge) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) ![Transformers](https://img.shields.io/badge/Transformers-FFC107?style=for-the-badge) ![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=for-the-badge)                |
| **Deployment**| ![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)                                                               |

---
## AI / ML Core

The intelligence of this assistant comes from a hybrid NLP pipeline that leverages both fine-tuned and pre-trained models.

### 1. Intent Classification
-   **Model:** A `distilbert-base-uncased` model was fine-tuned for this specific task.
-   **Method:** A parameter-efficient fine-tuning (PEFT) technique, **LoRA**, was used to adapt the model on a custom-generated dataset of over 1000 in-car commands.
-   **Deployment:** The final fine-tuned model is deployed as an independent microservice using a **Gradio API** on Hugging Face Spaces for maximum flexibility and decoupling.

### 2. Entity Extraction
-   **Mood:** The user's mood is inferred using a pre-trained emotion classification model (`bhadresh-savani/bert-base-go-emotion`).
-   **Names & Locations:** A pre-trained Named Entity Recognition (NER) model (`dslim/bert-base-NER`) is used to identify contacts and locations.
-   **Language:** A simple but effective rule-based keyword search is used to detect language preferences (e.g., "hindi", "punjabi").

---
## Running the Project Locally

Follow these steps to set up and run the project on your local machine.

### Prerequisites
-   Python 3.10+ and Conda
-   Node.js and npm
-   A GitHub account

### 1. Clone the Repository
```bash
git clone [https://github.com/Vishalchand0808/car-ai-assistant.git](https://github.com/Vishalchand0808/car-ai-assistant.git)
cd car-ai-assistant
````

### 2\. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate the conda environment:**
    ```bash
    conda create -n car-ai-env python=3.11
    conda activate car-ai-env
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create the `.env` file:**
    Create a file named `.env` inside the `backend` folder and add your API keys:
    ```env
    SPOTIFY_CLIENT_ID="YOUR_SPOTIFY_CLIENT_ID"
    SPOTIFY_CLIENT_SECRET="YOUR_SPOTIFY_CLIENT_SECRET"
    OPENWEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY"
    HF_SPACE_URL="YOUR_GRADIO_SPACE_URL"
    ```
5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

### 3\. Frontend Setup

1.  **Open a new terminal.**
2.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
3.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
4.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173`. Open this URL in your browser to use the application.

-----

## Challenges & Learnings

  - **Deployment Debugging:** The most significant challenge was deploying the fine-tuned model. The initial attempt using the automatic Inference API failed due to subtle configuration and library incompatibility issues. This led to a pragmatic pivot to a more robust deployment strategy using a Gradio Space, which provided a stable API endpoint.
  - **CORS Policies:** Successfully resolved complex Cross-Origin Resource Sharing (CORS) errors between the Vercel-hosted frontend and the Hugging Face-hosted backend, a critical skill in full-stack development.
  - **Git for Deployment:** Mastered advanced Git commands (`git subtree`) to handle the complex process of deploying a sub-directory of a monorepo to a separate hosting platform, including debugging and resolving unrelated histories with force pushes.

<!-- end list -->
