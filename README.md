Sure! Here's the `README.md` file for your project, following the provided template and including detailed instructions on how to run the project.

---

# SJEC, Vamanjoore - GabbarSinghs

- **Team Lead**: Nihaal Y K
- Joel Crasta
- Rachan Karkera

## Problem Statement

**Knowledge Distiller App**

## Instructions on Running Your Project

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.9** or higher
- **Node.js 14.x** or higher
- **npm** (comes with Node.js)
- **MongoDB** (local or remote instance)
- **Qdrant Vector Database** (local or remote instance)
- **Groq API Key** (you need to register for an API key)
- **Virtual Environment** tool (optional but recommended)

### Backend Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/knowledge-distiller-app.git
cd knowledge-distiller-app/code/backend
```

#### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage your Python dependencies.

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```ini
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_uri
QDRANT_URL=your_qdrant_url  # e.g., http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key  # Leave blank if not using an API key
```

Replace the placeholder values with your actual credentials and URLs.

#### 5. Run the Backend Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend server should now be running at `http://localhost:8000`.

### Frontend Setup

#### 1. Navigate to the Frontend Directory

Open a new terminal window and navigate to the frontend directory:

```bash
cd knowledge-distiller-app/code/frontend
```

#### 2. Install Node.js Dependencies

```bash
npm install
```

#### 3. Run the Frontend Development Server

```bash
npm run dev
```

The frontend application should now be running at `http://localhost:3000`.

### Using the Application

1. **Access the Frontend Interface**

   Open your web browser and navigate to `http://localhost:3000`.

2. **Upload and Process Documents**

   - Use the interface to upload a PDF document.
   - The frontend will send the extracted text to the backend API.
   - The backend processes the text, reconstructs formatting, generates embeddings, and creates a knowledge graph.
   - The knowledge graph is sent back to the frontend and visualized.

3. **Interact with the Knowledge Graph**

   - Explore the generated knowledge graph to understand the distilled information from your document.

### Notes

- **CORS Issues**: If you encounter any CORS (Cross-Origin Resource Sharing) issues, ensure that the `CORSMiddleware` is properly configured in your `main.py` file in the backend.

- **Port Configuration**: Ensure that both frontend and backend are running on the correct ports (`3000` for frontend and `8000` for backend). Adjust the ports in your configuration if necessary.

- **Database Connections**: Make sure that your MongoDB and Qdrant instances are running and accessible using the URIs provided in the `.env` file.

## References

- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Uvicorn Documentation**: [https://www.uvicorn.org/](https://www.uvicorn.org/)
- **Next.js Documentation**: [https://nextjs.org/docs](https://nextjs.org/docs)
- **React Documentation**: [https://reactjs.org/docs/getting-started.html](https://reactjs.org/docs/getting-started.html)
- **Tailwind CSS Documentation**: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
- **Groq API Documentation**: [Link to Groq API Documentation]
- **Qdrant Documentation**: [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)
- **MongoDB Documentation**: [https://docs.mongodb.com/](https://docs.mongodb.com/)
- **Sentence Transformers**: [https://www.sbert.net/](https://www.sbert.net/)

---

Feel free to customize and expand upon this README as needed for your project. If you have any questions or need further assistance, let me know!