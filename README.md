# ResuMate

**ResuMate** is a Python-based AI Resume Assistant designed to help users build and refine their resumes with AI-powered suggestions. It also offers **mock interview coaching** using personalized resume data and job descriptions.

The project is implemented using:
- Python
- MongoDB for data storage
- OpenAI API for AI-powered assistance

---

## Features

- **Resume Building**  
  Users can input and refine different resume sections using AI feedback.

- **Mock Interviews**  
  Generate personalized interview questions and receive feedback on your answers.

- **Resume Rendering**  
  View a clean, formatted version of your resume.

- **AI-Powered Suggestions**  
  Receive actionable feedback to improve resume content.

- **MongoDB Integration**  
  Store user data for easy access and updates.

---

## Prerequisites

Make sure the following are installed:

- Python 3.8+
- MongoDB
- `json` (built-in Python module)

---

## Usage

### 1. Run the Application

```bash
python hack_AI_final.py
```

### 2. Login or Create Profile

- Enter your **user ID** to log in.
- If the user does not exist, a new profile will be created in MongoDB.

> You can use a pre-built example by entering user ID: `"test_user"`

### 3. Build Your Resume

- Select a section to edit:  
  *Personal Info, Education, Professional Experience, Projects, Publications, or Skills*.
- Provide your content — the AI will return structured JSON and helpful suggestions.
- You can continue to refine the content through conversation.

### 4. Mock Interview Mode

- Provide a **job title** and **description**.
- AI will generate interview questions tailored to your resume.
- You answer → AI gives feedback.

### 5. View Resume

- Resume is rendered in a complete, formatted view based on stored data.

---

## API Reference

- **OpenAI API** — Used to generate suggestions and mock interview questions.
- **MongoDB** — Used for storing and retrieving structured resume data.

---

## Troubleshooting

**Mac SSL Certificate Error Fix**

If you encounter a certificate error (e.g. `CERTIFICATE_VERIFY_FAILED`), run:

```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

> Replace `3.x` with your installed Python version (e.g., `3.11`)

---

## Contributing

Contributions are welcome!  
Feel free to fork this repo and submit a pull request with a clear explanation of your changes.

---

## License

This project is licensed under the **MIT License**.  
See the [`LICENSE.md`](LICENSE.md) file for details.
