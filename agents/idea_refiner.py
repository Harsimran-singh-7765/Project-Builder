import os
import fitz
from crewai import Agent, Task, Crew, LLM
from google.generativeai import configure

from utils import ProjectInput
import warnings

# Ignore all DeprecationWarnings and UserWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from dotenv import load_dotenv

# Load the .env file from the ROOT directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))



print("GEMINI_API_KEY from env:", os.getenv("GEMINI_API_KEY"))
print("SERPER_API_KEY from env:", os.getenv("SERPER_API_KEY")) 

configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")  

from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool 
from langchain.tools import Tool
from langchain.agents import Tool


# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

def Refiner( input_data:ProjectInput) -> str:
    
    idea = input_data.idea_title
    desc = input_data.description
    members = input_data.team_members

   
    team_str = "\n".join([f"{m['name']} - {m['enrollment']}" for m in members])

    Idea_refiner = Agent(
        role="Senior Project Consultant",
        goal=(
            f"Your job is to transform a vague, student-submitted idea '{idea}' into a clear, feasible, and impressive project idea. "
            f"You must read '{idea}' and '{desc}' and then refine them, considering we have only these team members: {team_str}. "
            f"You will analyze the idea, search the web for existing solutions, and come up with a refined, innovative concept. "
            f"The final idea should include modules, real-world applications, and relevance to modern development. "
            f"The idea should be refined to suit a 1st year student project with properly defined features."
        ),
        backstory=(
            f"You are a renowned software architect... (rest remains same)"
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm  
    )
    Idea_refining = Task(
        description=(
            "Refine the student's initial vague idea into a well-structured and detailed project concept. "
            "Use online tools to research similar projects, current trends in , and open-source solutions. "
            "Then, using that knowledge, write a refined version of the idea which includes project scope, modules, tools, and technologies."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "A detailed  project summary of language according to {desc} that includes:\n"
            "1. A refined and improved project title\n"
            "2. A clear and concise description (max 2 paragraphs)\n"
            "3. basic structure or wirefreame of project or atleast list of possible functions made andstructure of it\n"
            "4. Suggested tools or libraries (e.g., Boost, OpenCV, etc.)\n"
            "5. Real-world relevance or use case of the project\n"
            "6. Skills required to build the project\n"
        ),
        agent=Idea_refiner
    ) 
    
    input = {
        "idea": idea,
        "user_description" : desc,
        "desc" : desc,
        "members": members
    }
    
    crew = Crew(
        agents=[Idea_refiner],
        tasks=[Idea_refining],
        verbose=False,
        inputs=input
        
    )
    
    result = crew.kickoff(input)
    print("Idea_refiner_success\n\n")
    return result.raw



