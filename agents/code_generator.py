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

def generate_code(input_data:ProjectInput):
    idea = input_data.idea_title
    desc = input_data.description
    members = input_data.team_members
    refined_idea = input_data.refined_idea
    
    WorkEnhancer = Agent(
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
    
    ManagerAgent = Agent(
        role="Technical Work Distribution Manager",
        goal=(
            "Take the structured breakdown from the WorkEnhancer agent and interpret it carefully. Based on the plan and the available team members: {members}, "
            "create a precise work distribution strategy. Break the total project into modular coding tasks, and intelligently assign them "
            "to the seven WorkerAgents. Your task is to ensure that the logic of the project is preserved while distributing the tasks fairly and efficiently. "
            "Also, try to balance complexity between agents and ensure no overlapping work is assigned. The goal is to streamline collaboration "
            "so that the final code is coherent, scalable, and maintainable."
            "You need to ensure that user gets a complete code in a single file unless creation of other files is essential and "
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You are an expert in software engineering leadership. Having worked as a technical project manager for elite coding bootcamps, "
            "you excel in interpreting project plans and assigning tasks to junior developers in a logical and efficient manner. You understand "
            "code structure, modularity, and design patterns deeply. Your job is to ensure the team of WorkerAgents functions like a well-oiled machine, "
            "with each one clear on their responsibilities. You focus on collaboration and clean architecture to get academic-quality code with real-world readiness."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm
    )



    WorkerAgent1 = Agent(
        role="Senior Software Developer 1",
        goal=(
            "Take any task assigned by the Manager and write high-quality code based on the instructions. "
            "If the description mentions a programming language (e.g., C or C++), make sure to use that language strictly. "
            "The output should be clean, functional, and follow best practices."
            "write a clean code and a code that works with logic "
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You are a highly experienced  software developer who has contributed to large-scale open source and industrial projects. "
            "You understand low-level optimization, memory management, and clean architecture. You write readable and robust code."
        ),
        verbose=False,
        allow_delegation=False,
        
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    WorkerAgent2 = Agent(
        role="Senior Software Developer 2",
        goal=WorkerAgent1.goal,
        backstory=(
            "You have worked at startups and Fortune 500 companies alike, known for your ability to write fast, clean code in C and C++ or any language of the world. "
            "You love transforming rough ideas into polished, production-ready programs. You think like a compiler."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    WorkerAgent3 = Agent(
        role="Senior Software Developer 3",
        goal=WorkerAgent1.goal,
        backstory=(
            "You're a all languages expert who has trained hundreds of students and interns. Your focus is on clean syntax, avoiding redundancy, "
            "and always ensuring the code is logically correct and ready to compile without errors."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    WorkerAgent4 = Agent(
        role="Senior Software Developer 4",
        goal=WorkerAgent1.goal,
        backstory=(
            "With years of experience in embedded systems and OS-level programming, you’re skilled at both micro-level performance tuning "
            "and macro-level software structure. You love coding challenges and systems design equally."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    WorkerAgent5 = Agent(
        role="Senior Software Developer 5",
        goal=WorkerAgent1.goal,
        backstory=(
            "You have participated in competitive programming and contributed to CP libraries. Your code is known for handling edge cases "
            "and extreme inputs with ease. You're also great at writing modular and reusable code."
        ),
        verbose=False,
        tools=[search_tool, scrape_tool],
        allow_delegation=False,
        llm=llm
    )

    WorkerAgent6 = Agent(
        role="Senior Software Developer 6",
        goal=WorkerAgent1.goal,
        backstory=(
            "You’ve worked on game engines and graphics-heavy applications. You deeply understand memory, performance, and write tight  code. "
            "You ensure the structure is scalable and readable even in large projects."
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    WorkerAgent7 = Agent(
        role="Senior Software Developer 7",
        goal=WorkerAgent1.goal,
        backstory=(
            "You're the jack-of-all-trades coder. Whether it's C, C++,python,java,next.js,typescript STL, or even lower-level bit manipulation, you do it all. "
            "You’ve been part of AI systems, OS kernels, and even game logic layers. You take pride in precision and excellence."
            "You use language u are assinged in the {desc}"
        ),
        verbose=False,
        allow_delegation=False,
        tools=[search_tool, scrape_tool],
        llm=llm
    )

    CodeEditorAgent = Agent(
        role="Final Code Editor and Integrator",
        goal=(
            "You will receive code snippets written by seven developers, each representing a different part of the overall project. "
            "Your job is to smartly integrate all pieces into one coherent codebase. Make sure the code compiles and follows standard conventions. "
            "If any syntax issues, conflicts, or integration mismatches arise, you must resolve them automatically. "
            "Output a single, ready-to-run program file (preferably in C or the chosen language)."
            "You will insure all code given to you are working even input and test cases and ensure that code is in a single {idea}.cpp/{idea}.c unless any other language is mentioned "
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        backstory=(
            "You're a senior software engineer known for your mastery in handling large-scale code merges and ensuring everything runs smoothly. "
            "You've worked in DevOps, CI/CD, and collaborative coding environments where developers work on separate modules. "
            "You don't just stitch code — you optimize, sanitize, and ensure that the final output is flawless and ready to compile."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm
    )
    
    UIDivFormatterAgent = Agent(
        role="Code UI Formatter and Presenter",
        goal=(
            "Your role is to take the final integrated code and format it in a well-structured <div> format. "
            "This is for displaying the code nicely in a UI or documentation page. You must break down the code module-wise using comments "
            "and present each section inside a separate styled div, with appropriate headings and syntax highlighting (if required)."
            "You are not supposed to geneate a HTML FILE, you will generate a single div tag which will  consist of all data "
        ),  
        backstory=(
            "You are a creative frontend engineer and technical content designer. You specialize in turning raw code into beautifully formatted, "
            "readable components for websites, documentation, and showcases. You've worked with UI teams, IDE plugins, and Markdown renderers. "
            "Now, you're here to give the final project code a professional and visually understandable look."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

    WorkEnhancerTask = Task(
        description=(
            "Analyze the student's project idea, description, and number of team members. Create a deep, production-level breakdown that includes:\n"
            "- What the project should do\n"
            "- How big the codebase should be (based on members)\n"
            "- Key classes, functions, modules\n"
            "- Overall C++ design principles to follow\n"
            "- Style, libraries, or data structures to use"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "A structured breakdown including:\n"
            "1. Estimated code length based on team size\n"
            "2. Project structure (Modules, Files, Folders)\n"
            "3. Key features to include\n"
            "4.C++ design considerations (OOP, STL, etc.)"
        ),
        agent=WorkEnhancer
    )
    ManagerTask = Task(
        description=(
            "Take the output from WorkEnhancer and distribute tasks to 7 worker developers.\n"
            "Create 7 logical parts of the code such that each part is complete and implementable independently.\n"
            "Assign file/module names, responsibilities, and hints for each developer.\n"
            "Ensure fair division and no overlap."
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "A developer-wise task assignment , give them task of codes of a same file:\n"
            "1. Worker1: Task A, File: `x.cpp`\n"
            "2. Worker2: Task B, File: `x.cpp`\n"
            "...\n"
            "7. Worker7: Task G, File: `x.cpp`\n"
            "Each with short description, goal, logic expected."
        ),
        agent=ManagerAgent
    )
    
    Worker1Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent1
    )
    Worker2Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent2
    )
    Worker3Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent3
    )
    Worker4Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent4
    )
    Worker5Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent5
    )

    Worker6Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent6
    )
    Worker7Task = Task(
        description=(
            "You are a dedicated  developer. Based on the task assigned to you by the ManagerAgent, write a complete and working  file/module. "
            "Include only your assigned part, write clean code, use appropriate headers, and follow best practices. Do not write placeholder or dummy code."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1.  code implementing your task\n"
            "2. Use of proper class/function structure\n"
            "3. Comments for clarity\n"
            "4. No main() unless assigned\n"
            "5. Compilable, modular, and high quality"
        ),
        agent=WorkerAgent7
    )
    CodeEditorTask = Task(
        description=(
            "Your job is to combine all 7 workers' code files into a single project. Ensure the includes, class dependencies, and main function work correctly. "
            "Fix any errors in compilation, resolve linking problems, and return a ready-to-run single  file or project folder structure."
            "You should use the language mentioned in the {desc} else assume C++"
        ),
        expected_output=(
            "You should use the language mentioned in the {desc} else assume C++"
            "1. Fully integrated  code\n"
            "2. Working main() if applicable\n"
            "3. All classes and functions linked\n"
            "4. No syntax or linkage issues\n"
            "5. Clear module headers and organization"
        ),
        agent=CodeEditorAgent
    )
    input = {
        "idea": idea,
        "User_discription" : desc,
        "members": members,
        "desc":desc
    }
    CodeFormatterTask = Task(
        description=(
            "Take the final combined code and convert it into a well-formatted dic tAG. Use proper HTML sections, code blocks, and syntax highlighting."
            "Each file/module should appear in its own <div> or <section>."
            "code should look good not fuzzy add line spacing if needed else keep it professional"
        ),
        expected_output=(
            "1.DIV TAG of full code , add sections if needed \n"
            "2. Code wrapped in <pre><code> blocks\n"
            "3. Use <h3>, <p>, <hr> for readability\n"
            "4. Beautiful, copy-ready documentation"
        ),
        agent=UIDivFormatterAgent
    )

    crew = Crew(
        agents=[
            WorkEnhancer,
            ManagerAgent,
            WorkerAgent1,
            WorkerAgent2,
            WorkerAgent3,
            WorkerAgent4,
            WorkerAgent5,
            WorkerAgent6,
            WorkerAgent7,
            CodeEditorAgent,
            UIDivFormatterAgent
        ],
        tasks=[
            WorkEnhancerTask,
            ManagerTask,
            Worker1Task,
            Worker2Task,
            Worker3Task,
            Worker4Task,
            Worker5Task,
            Worker6Task,
            Worker7Task,
            CodeEditorTask,
            CodeFormatterTask
        ],
        verbose=True,
        concurrent_tasks=True,
        inputs = input
    )

    output = crew.kickoff(input)



    
    return output.raw