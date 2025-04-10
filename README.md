
# 🚀 THE PROJECT BUILDER



**THE ULTIMATE AI-POWERED PROJECT HELPER 🔧 + 🧠**

> Whether you're stuck on a college project or just exploring ideas, this smart tool cuts your workload in half — and boosts your creativity with the power of AI.

---

## 🧠 What it does

Just give it your:
- ✅ **Project Idea / Description**
- 👥 **Team Member Names**

And it auto-generates:
- 📝 A full **Synopsis**
- 📅 **Roadmap & Timeline**
- 💻 **Customized Code**
- 📌 **Smart Project Tips**
- 📄 A clean **PDF** with all content packed beautifully

---

## 🛠️ Tech Stack

- 🐍 **Python**
- 🤖 **CrewAI** – Multi-agent framework
- ✨ **OpenAI / HuggingFace / Gemini APIs**
- 🧾 **xhtml2pdf** + **PyMuPDF (fitz)** – PDF generation
- 🌐 **Flask** – Web app backend
- 🎨 **HTML/CSS/JS** – Simple and clean frontend

---

## 🗂️ Project Structure

```
THE_PROJECT_BUILDER/
├── agents/                   # AI agents for idea refining, synopsis generation, etc.
│   ├── idea_refiner.py
│   ├── synopsis_generator.py
│   ├── project_tips.py
│   └── roadmap_creator.py
│   └── code_generator.py

├── data/                     # Data folder for training and extraction
│   └── Train_data/
│       └── pdf_exraction.py
|       └── Synopsis.pdf


├── static/                   # Frontend static files
│   ├── css/
│   ├── js/
│   ├── images/
│   └── output_pdfs/          # Exported PDFs via web interface

├── templates/                # HTML templates for rendering pages
│   └── index.html

├── utils/                    # Utility scripts
│   ├── _init.py
│   └── pdf_generator.py

├── app.py                    # Main Flask app

├── .env                      # Environment variables (e.g., API keys)
├── .gitignore                # Files to ignore during git pushes
├── requirements.txt          # Python dependencies
└── README.md                 # This file – your project documentation

```

## ⚙️ How to Run

1. **Clone the repo**
```bash
git clone https://github.com/Harsimran-singh-7765/Project-Builder.git
cd Project-Builder
```


2. **install requirements**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a .env file and add:**
    ```env
    SERPER_API_KEY="your_key_here"
    GEMINI_API_KEY="your_gemini_key_here"
    ```

4. **RUN :**
    ```bash
      python app.py
    ```

---

---

## 👤 Author  
**Made with ❤️ by Harsimran Singh**

Feel free to:

- 💫 **Star** this repo if it helped you  
- 🍴 **Fork** it and make it even better  
- 🤝 **Contribute** by raising PRs  
- 👋 Or just say hi and connect!

> “Code hard, dream bigger, and let AI handle the boring stuff!”






