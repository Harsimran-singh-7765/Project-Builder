from flask import Flask, render_template, request, send_file,session
from utils import ProjectInput,QuestionInput
from agents.idea_refiner import Refiner
from agents.synopsis_generator import generate_synopsis
from agents.roadmap_creator import generate_roadmap
from utils.pdf_generator import html_to_pdf
from agents.code_generator import generate_code
from agents.project_tips import generate_project_tips
import warnings
import os



os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

app.secret_key = "INPUT"  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF_PATH = os.path.join(BASE_DIR, "static", "output_pdfs", "synopsis.pdf")
OUTPUT_PDF_PATH_RoadMAP = os.path.join(BASE_DIR, "static", "output_pdfs", "Roadmap.pdf")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        idea = request.form.get('idea')
        description = request.form.get('description')
        members_raw = request.form.get('members')
        task = request.form.get('task')

        # Convert raw team member input to list of dicts
        team_members = []
        for line in members_raw.strip().split(','):
            if '-' in line:
                name, enrollment = line.split('-', 1)
                team_members.append({
                    "name": name.strip(),
                    "enrollment": enrollment.strip()
                })

        input_data = ProjectInput(
            idea_title=idea,
            description=description,
            team_members=team_members,
            refined_idea=""
        )
        
 

        refined_idea = Refiner(input_data)
        input_data.refined_idea = refined_idea

        if task == "generate_synopsis":
            result = generate_synopsis(input_data)
            result = result.replace("```html", "").replace("```", "").strip()
            html_to_pdf(result, OUTPUT_PDF_PATH)    
            download_url = "/static/output_pdfs/synopsis.pdf"
            return render_template("index.html", result=result, download_link=download_url)
            
        elif task == "generate_roadmap":
            result = generate_roadmap(input_data)
            result = result.replace("```html", "").replace("```", "").strip()
            
        
            html_to_pdf(result, OUTPUT_PDF_PATH_RoadMAP)

            
            download_url = "/static/output_pdfs/Roadmap.pdf"
            return render_template("index.html", result=result, download_link=download_url)
        
        elif task == "generate_code":
            result = generate_code(input_data)
            result = result.replace("```html", "").replace("```", "").strip()
            
        
            html_to_pdf(result, OUTPUT_PDF_PATH_RoadMAP)

           
            download_url = "/static/output_pdfs/Roadmap.pdf"
            return render_template("index.html", result=result, download_link=download_url)
        
        elif task == "submit_tips":
            
            question = request.form.get('question')
            
            if not question:
                return render_template("index.html", result="<p style='color:red;'>Please enter a valid question.</p>")
            
            if 'chat_history' not in session:
                session['chat_history'] = []
            print("1\n")
            input_data_dict = {
                "idea": input_data.idea_title,
                "description": input_data.description,
                "refined_idea": input_data.refined_idea,
                "members": input_data.team_members,
            }

            
            full_input = QuestionInput(
            project=input_data,
            question=question
                        
            )
            full_input.history = session['chat_history']
            print("2\n")
            result = generate_project_tips(full_input)

            
            session['chat_history'].append({"q": question, "a": result})
            session.modified = True
            
            full_input.history = session['chat_history']

            return render_template("index.html", result=result, chat_history=session['chat_history'])
        
        return render_template("index.html", result="Invalid task selected.")

    except Exception as e:
        return render_template("index.html", result=f"<p style='color:red;'>Error: {str(e)}</p>")



if __name__ == '__main__':
    app.run(debug=True)
