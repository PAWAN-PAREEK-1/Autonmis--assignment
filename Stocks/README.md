****Set up the backend:****

**1.Navigate to the backend folder:**

cd backend

**2.Create a Python virtual environment:**

python3 -m venv venv

**3.Activate the virtual environment:**

On Windows: venv\Scripts\activate

**4.Install the required dependencies:**

pip install -r requirements.txt

**5.Start the backend server:**

uvicorn main:app --reload


****Set up the frontend:****

**1.Navigate to the frontend folder:**

cd ../frontend

**2.Install the frontend dependencies:**

npm install

**3.Run the frontend development server:**
npm run dev

**Verify the application:**

Open http://localhost:3000 in your browser to see the frontend.
The backend will be running at http://localhost:8000.
