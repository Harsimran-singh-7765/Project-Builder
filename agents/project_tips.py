import os
import fitz
from crewai import Agent, Task, Crew, LLM
from google.generativeai import configure
from utils import ProjectInput,QuestionInput
from dotenv import load_dotenv

# Load the .env file from the ROOT directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")

def generate_project_tips(full_input:  QuestionInput) -> str:
    print("3\n")
    idea = full_input.project.idea_title
    desc = full_input.project.description
    refined_idea = full_input.project.refined_idea
    team_members = full_input.project.team_members
    question = full_input.question
    history = full_input.history


    
    chat_log = "\n".join([f"Q: {msg["q"]}\nA: {msg["a"]}" for msg in history])
    



    tip_guide = Agent(
        role=" Project Guide,helpwer",
        goal=(
            "You should use the language mentioned in the {desc} else assume C++"
            "Help students by answering their project-related questions {question} accurately and creatively. "
            "Use the provided project context {idea},{refined_idea} and in accordance with chat history {chat_log} to keep answers consistent and build upon previous suggestions."
        ),
        backstory=(
            "You are a smart, interactive AI assistant designed to help students with technical and creative guidance on their  projects. "
            "You're trained on thousands of student queries, project building steps, and real-world problem-solving examples. "
            "You're meant to simulate the behavior of an expert professor who knows how to keep continuity in discussions."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    EditorAgent = Agent(
        role="Technical Content Editor",
        goal=(
            "Your job is to take all the inputs provided from previous agents — including refined idea, planning, function list, "
            "timeline, work distribution, teacher tips, and format them into a beautiful, professional-looking HTML structure "
            "suitable for displaying on a project showcase website."
            "Use <div>, <h2>, <p>, <ul>, <table> and other HTML elements where needed."
            "Maintain readability, professional style, and make it look like a complete 2000+ word academic roadmap presentation."
        ),
        backstory=(
            "You are a seasoned technical editor who specializes in converting raw, unformatted content into high-quality, "
            "HTML-compatible academic and technical documentation. "
            "You've worked with publishing houses, educational platforms, and project showcase websites. "
            "You have a strong sense of structure, presentation, and formatting — and you know how to make content clean, readable, and visually appealing. "
            "You ensure there are no duplicate ideas, everything flows well, and the end result looks like a professional document."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm
    )    

    
    tip_task = Task(
        description=(
            "Based on the student's question {question} and the given project context {idea},{refined_idea}  + Q&A history {chat_log}, respond with a clear, creative, and helpful answer. "
            "Maintain continuity with previous answers and make sure the guidance is practically applicable."
        ),
        expected_output=(
            "A well-written, helpful answer of maximum 60 words  to the question that:\n"
            "1. Stays within project scope\n"
            "2. Refers back to previous Q&A if relevant\n"
            "3. Gives practical, implementable advice\n"
            "4. Suggests tools, structure, or improvement where needed"
        ),
        agent=tip_guide
    )

    FinalEditing = Task(
        description=(
            "Your job is to collect all the outputs from previous agents — refined idea, planning, function map, timeline, and teacher advice — "
            "and compile them into a professional div tag suitable for submission or website display. Use good formatting practices, HTML structure, and ensure visual flow."
        ),
        expected_output=(
            "A final Div TAg  that contains:\n"
            "1. Title and project introduction\n"
            "2. Module-wise planning with headers and sections\n"
            "3. Properly formatted function and class definitions\n"
            "4. Timeline as a clean <table> or <ul>\n"
            "5. Mentor’s advice as a special <blockquote> or styled <div>\n"
            "6. Overall styling with good use of tags like <h2>, <p>, <code>, <ul>, <table>"
        ),
        agent=EditorAgent
    )

    # Inputs to share with the crew
    crew_inputs = {
        "idea": idea,
        "desc": desc,
        "refined_idea": refined_idea,
        "team_members": team_members,
        "question": question,
        "history": history,
        "chat_log": chat_log
    }


    # Create the crew and run the task
    crew = Crew(
        agents=[tip_guide,EditorAgent],
        tasks=[tip_task,FinalEditing],
        verbose=True,
        inputs=crew_inputs
    )

    result = crew.kickoff(crew_inputs)
    return result.raw
