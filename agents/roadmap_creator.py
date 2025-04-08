import os
import fitz
from crewai import Agent, Task, Crew, LLM
from google.generativeai import configure
from utils import ProjectInput
from dotenv import load_dotenv

# Load the .env file from the ROOT directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
configure(api_key=os.environ["GEMINI_API_KEY"])
llm = LLM(model="gemini/gemini-1.5-flash")

from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool 
from langchain.tools import Tool
from langchain.agents import Tool


# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

def generate_roadmap(input_data:ProjectInput): 
    idea = input_data.idea_title
    desc = input_data.description
    members = input_data.team_members
    refined_idea = input_data.refined_idea
    
    Workenhancer = Agent(
        role="Project Planner and Enhancer",
        goal=(
            "Your job is to analyze the student's project idea: {idea}, understand the user's description: {User_discription}, "
            "and considering the available team members: {members}, create a highly structured and technically detailed breakdown. "
            "This breakdown must define clear goals, identify technical components, suggest enhancements, and provide the foundation "
            "for further planning, development, and work distribution. Your output must help convert this idea into a production-level plan."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You are a master project planner who has worked with Fortune 500 companies, helping them transform raw concepts "
            "into scalable digital products. You specialize in early-stage planning, requirement analysis, and technical feasibility. "
            "You have a background in software engineering, systems design, and project management, and you're known for breaking down "
            "chaotic student ideas into polished, practical, and academically strong projects. You think like a developer, a professor, "
            "and a visionary - all in one. You've been hired to ensure the student starts with the right foundation."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    Functions_Builder = Agent(
        role="Asynchronous Functional Architect",
        goal=(
            "Your job is to read the refined project idea based on the original: {idea}, and user description: {User_discription}, "
            "and generate a full list of possible  functions, classes, and modules that would be needed to implement the project. "
            "Your output must cover functional decomposition, i.e., what features the project needs and how each can be implemented in . "
            "Ensure modular programming, object-oriented principles, file handling, and realistic implementation paths are considered."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You are an expert developer who has written thousands of modular programs and designed full-fledged systems for educational, "
            "commercial, and embedded environments. You specialize in decomposing big problems into small, testable, efficient functions. "
            "You follow best practices in naming, commenting, and class design. You are currently mentoring college students on building "
            "projects that are modular, testable, and aligned with first-year curriculum but still impressive in quality."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )
    
    TimelinePlanner = Agent(
        role="Milestone-Based Timeline Expert",
        goal=(
            "Your job is to analyze the project idea: {idea}, the user's description: {User_discription}, and the team size: {members}, "
            "then break down the entire project into a realistic, week-by-week or phase-by-phase timeline. "
            "For each step, define deliverables, expected outcomes, required skills, and tools to be used. "
            "Ensure this timeline is both realistic for students and also sufficient to complete a well-functioning project."
            "Assume a completion span in normal case 2 week and increase according to diffculty of {idea}"
        ),
        backstory=(
            "You are a professional project timeline architect who has built detailed schedules for both academic and real-world software teams. "
            "You've worked with startups, hackathons, college capstones, and R&D teams, helping them optimize time and resources. "
            "You specialize in student-based timelines where limited time, skills, and experience must still produce solid outcomes. "
            "You are now working with a group of students to create a highly actionable project schedule from scratch."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[],
        llm=llm
    )


    TeacherAgent = Agent(
        role="Project Mentor and Guide",
        goal=(
            "You are assigned to guide students in starting and completing their project. "
            "Based on the refined idea: {idea}, the detailed description: {User_discription}, and the team size {members}, "
            "you will provide valuable mentorship advice on how to begin, what tools or libraries to use, how to divide time, "
            "how to avoid common mistakes, and how to keep the project creative and successful."
            "Focus on motivating and encouraging students like a real-life mentor would, and keep the tone friendly yet professional."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You are a highly respected university professor who has mentored thousands of students across 10+ years in computer science and software development. "
            "You understand the challenges students face — lack of direction, confusion in planning, and teamwork issues. "
            "You are empathetic, highly experienced, and know exactly how to make students believe in themselves. "
            "You often interact with student teams in college fests, hackathons, and classroom sessions. "
            "Now, you’ve been assigned to act as a project mentor for a team with a  based idea. "
            "You want to help them not just complete the project but grow through it."
        ),
        verbose=False,
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

    InitialPlanning = Task(
        description=(
            "Understand the refined project idea and convert it into a complete structured plan. "
            "Divide the idea into clear modules and sub-modules, outline each part’s technical requirements, and identify enhancements or features. "
            "Use your project planning knowledge to ensure it's logical, achievable, and technically sound for student-level implementation."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "A detailed planning document that includes:\n"
            "1. Logical module-wise breakdown of the entire project\n"
            "2. Technical summary of what each module does\n"
            "3. Suggestions for additional features and improvements\n"
            "4. Skill level required per module\n"
            "5. Tools/libraries to be used (if applicable)\n"
            "6. Potential risks and early solutions"
        ),
        agent=Workenhancer
    )
    
    FunctionMapping = Task(
        description=(
            "Based on the refined idea and planning, generate a detailed map of all the functions and classes needed in the project. "
            "Use proper  syntax of language mentioned in {desc}, object-oriented principles, and modular design thinking. Make sure each function has a defined purpose and fits into the system cleanly."
        ),
        expected_output=(
            "A full function-class mapping document including:\n"
            "1. List of all required functions with names and purposes\n"
            "2. Parameters and return types\n"
            "3. Possible header file & source file separation\n"
            "4. Class definitions, member variables, and methods\n"
            "5. Relationships between modules/classes\n"
            "6. At least 2 example code snippets"
        ),
        agent=Functions_Builder
    )
    
    TimelinePlannerTask = Task(
        description=(
            "Always consider minimu time as 2-3 weeks depending on the dificulty of the {idea}"
            "Break down the project into a clear and achievable week-wise timeline. "
            "Divide work in a way that aligns with typical college schedules. "
            "Include which modules/functions are to be built when, what is expected each week, and what tools/resources will be needed."
        ),
        expected_output=(
            "A realistic, milestone-based project timeline with:\n"
            "1. Weekly goals and milestones\n"
            "2. Module/function names to be completed in each phase\n"
            "3. Required tools/libraries/software per week\n"
            "4. Challenges to expect and how to tackle them\n"
            "5. Deliverables for each checkpoint\n"
            "6. Final review and buffer period"
        ),
        agent=TimelinePlanner
    )

    TeacherAdvice = Task(
        description=(
            "Act like a real-life project mentor. Read the entire refined idea, planning, and timeline. "
            "Give personal, practical guidance to students about how to proceed, what mindset to keep, and how to overcome common obstacles. "
            "Keep tone motivating, friendly, yet technically helpful."
        ),
        expected_output=(
            "A mentorship note that includes:\n"
            "1. Best practices to follow while building the project\n"
            "2. Motivational advice and team coordination tips\n"
            "3. Common mistakes students make and how to avoid them\n"
            "4. How to handle bugs or errors\n"
            "5. Suggestions for extra credit or innovation\n"
            "6. Recommended habits to build productivity"
        ),
        agent=TeacherAgent
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

    input = {
        "idea": idea,
        "User_discription" : desc,
        "members": members,
        "desc":desc
    }
    
    crew = Crew(
        
        agents=[Workenhancer, Functions_Builder, TimelinePlanner, TeacherAgent, EditorAgent],
        tasks=[InitialPlanning, FunctionMapping, TimelinePlannerTask, TeacherAdvice, FinalEditing],
        verbose=True,
        concurrent_tasks=True  
    )

    result = crew.kickoff(input)
        
    return result.raw


