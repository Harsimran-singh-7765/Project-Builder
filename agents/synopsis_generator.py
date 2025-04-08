import os
import fitz
from crewai import Agent, Task, Crew, LLM
from google.generativeai import configure
from utils import ProjectInput
from data.Train_data.pdf_exraction import data_pdf
import warnings
import os
from dotenv import load_dotenv

# Load the .env file from the ROOT directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Now safely get the key
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")

configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")

# Extract sample data
data = data_pdf()
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def generate_synopsis(input_data: ProjectInput) -> dict:
    idea = input_data.idea_title
    desc = input_data.description
    members = input_data.team_members
    refined_idea = input_data.refined_idea

    synopsis_input = {
        "idea": idea,
        "desc": desc,
        "team_members": members,
        "refined_idea": refined_idea,
        "sample_format_text": data
    }

    sample_structure = """
    1. Title of the Project
    2. Details of Team (Names and Roll numbers)
    3. Abstract of the project (Max. 500 words)
    4. Topics of SDF used (e.g., pointers, loops, algorithms)(In Points)
    5. (Libraries you will need use the heading) "Header Files and Libraries(in POINTS)"
    """

    # ---- Synopsis Generator Agent ---- #
    synopsis_agent = Agent(
        role="Synopsis Writer",
        goal=(
            f"Your task is to write an academic synopsis based on this new project idea:\n\n"
            f"Title: {idea}\nDescription: {desc}\nTeam Members: {members}\n\n"
            f"You need to understand which language user want to use acc to {desc}"
            f"Use this sample format structure:\n{sample_structure}\n"
            f"Maintain academic tone, clean formatting, and use refined idea: {refined_idea}.\n"
            f"The original sample synopsis to follow is:\n{data[:800]}...\n"
            f"Make sure output is compact enough to fit on one page."
        ),
        backstory=(
            f"You are an expert academic writer. Your job is to write synopses that mimic sample formats. "
            f"Follow the academic tone, sections, and style shown in this sample:\n\n{data[:500]}...\n"
            f"Include the refined idea: {refined_idea}."
        ),
        allow_delegation=False,
        verbose=False,
        llm=llm
    )

    
    editor = Agent(
        role="Format Text",
        goal="Take the synopsis and format it as a single clean <div> using semantic HTML for modern websites.",
        backstory=(
            "You're a top UI/UX designer. Your job is to format academic content into clean HTML. "
            "Focus on visual clarity using <h1>, <h2>, <p>, <ul>, <b>, <u>, etc. Use Google Fonts style."
            "Keep it minimal, modern, and responsive-ready. Output only the HTML <div>, no comments."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    # ---- Task 1: Generate Synopsis ---- #
    synopsis_generation = Task(
        description=(
            f"Generate an academic synopsis for the following:\n"
            f"Project Title: {idea}\n"
            f"Description: {desc}\n"
            f"Refined Idea: {refined_idea}\n"
            f"Team Members: {members}\n\n"
            f"Sample format to follow:\n{sample_structure}\n"
            f"Follow the structure exactly. Output should include all sections properly marked with headings and no extra spaces after each componenet."
            f"The output should be according to input language stated in {desc}"
        ),
        agent=synopsis_agent,
        expected_output=(
            "Structured academic synopsis with:\n"
            "1. Title of the Project\n"
            "2. Team Member Details\n"
            "3. Abstract (max 500 words)\n"
            "4. Topics of SDF Used (include pointers, loops, algorithms) (IN POINTS)"
            "5. Libraries you will or might USE Use (Cmath etc (IN POINTS)"
        ),
        inputs=synopsis_input
    )

    # ---- Task 2: Format into HTML ---- #
    TextFormatterTask = Task(
        description=(
            "Take the raw synopsis text and format it into clean HTML inside a single <div>. Use:\n"
            "- <h1> for Project Title\n"
            "- <h2> for sections like Abstract, Team Members, etc.\n"
            "- <p>, <ul>, <li>, <b>, <u> where needed\n"
            "Do NOT include full HTML boilerplate. Only return a single <div> containing formatted content. "
            "Ensure readability and responsive design. Keep it clean, professional, and elegant. "
            "Use styling inspired by Google Fonts."
            "Keep the desin compact add no style which willl change line spacing in the div"
        ),
        expected_output=(
            "A single <div> containing the formatted synopsis with proper use of headings, paragraphs, bold and underline tags. "
            "Follow this structure:\n"
            "1. Title of the Project\n"
            "2. Details of Team (Name, Roll Numbers)\n"
            "3. Abstract (within 250 words)\n"
            "4. Topics of SDF used (basic ones like loops, pointers)"
            "NOTE: MAKE IT LOOK PROFESSIONAL DON'T ADD USELESS <br>"
            
        ),
        agent=editor,
    )

    # ---- Crew Setup ---- #
    crew = Crew(
        agent=[synopsis_agent, editor],
        tasks=[synopsis_generation, TextFormatterTask],
        verbose=False,
        inputs=synopsis_input
    )

    result = crew.kickoff()
    print("synopsis_success\n\n")
    return result.raw
