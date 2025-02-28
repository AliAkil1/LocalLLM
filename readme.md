

# **LangChain + Streamlit with DeepSeek-R1**

This project demonstrates how to use the LangChain Python library with a locally hosted Ollama server running the `deepseek-r1:1.5b` model. The app is built using Streamlit, allowing users to interact with the model through a web interface.

---

## **Setup Instructions**

### 1. **Create a Virtual Environment**
To keep your dependencies isolated, create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. **Install Required Libraries**
Install all dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. **Run the Streamlit App**
Start the Streamlit app by running:
```bash
streamlit run app.py
```

Once the app is running, open your browser and go to `http://localhost:8501` to interact with the model.

---

## **Prerequisites**
- Install and set up [Ollama](https://ollama.com) on your machine.
- Download the `deepseek-r1:1.5b` model by running:
  ```bash
  ollama pull deepseek-r1:1.5b
  ```
- Start the Ollama server before running the app:
  ```bash
  ollama serve
  ```

---

Feel free to customize or extend this project! 😊

--- 

This `README.md` file provides clear instructions for setting up and running your project while ensuring users know how to prepare their environment properly.

---
Answer from Perplexity: pplx.ai/share