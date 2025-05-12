# EduGPT: An AI student assistant chatbot


## About

EduGPT is a RAG-based chatbot designed to provide accurate, context-aware answers by retrieving information only from uploaded documents.


## Main Functionalities

**1. Document-Based Information Retrieval**
Retrieves and generate context-aligned answers from educator-uploaded materials

2. Real-Time Document Upload
Students can upload their own personal notes or reference materials so they can utilize the chatbot for personalized learning

3. Display References
Shows source document name, page numbers, text, and clickable links so users can verify and trace responses back to original content


## Usage

1. Navigate to the project directory 
   ```bash
   cd EduGPT
   ```

3. Create new virtual environment and activate environment

   ```bash
   python3.11 -m venv projectenv
   projectenv\Scripts\Activate.ps1
   ```

4. Install required libraries

   ```bash
   pip install -r requirements.txt
   ```

5. Upload documents to be pre-processed under data/docs and run:

   ```bash
   python src\upload_data_manually.py
   ```

6. Run the application:

In terminal 1:

   ```bash
   python src\serve.py
   ```

In terminal 2:

   ```bash
   python src\raggpt_app.py
   ```



