import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from crewai.llms.providers.gemini.completion import GeminiCompletion
from dotenv import load_dotenv


load_dotenv()

# 1. ENVIRONMENT CONFIGURATION & KEYS

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SERPER_API_KEY= os.getenv('SERPER_API_KEY')

# Initialize the official CrewAI LLM wrapper to route queries to Gemini
#  using gemini-2.5-flash for maximum tracking speed and reasoning quality
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=GEMINI_API_KEY
)

# Initialize the automated web search engine tool for our researcher agent
web_search_tool = SerperDevTool()

# 2. AGENT DEFINITIONS (The Roles & Personalities)


# AGENT 1: The Researcher (Armed with Web Search capabilities)
researcher_agent = Agent(
    role="Senior Research Analyst",
    goal="Scrape the internet to uncover breaking developments, facts, and metrics on a specified topic.",
    backstory=(
        "You are an expert digital private investigator. You look past surface headlines "
        "to find the true source technical data, expert quotes, and key chronological points."
    ),
    tools=[web_search_tool],  # Giving this agent the ability to browse the web!
    llm=gemini_llm,
    verbose=True,  # This prints the agent's real-time internal thinking process to your terminal
    allow_delegation=False
)

# AGENT 2: The Writer (Focuses on language polish and formatting)
writer_agent = Agent(
    role="Technical Content Editor",
    goal="Synthesize raw technical research notes into an elegant, clear, and highly engaging Markdown report.",
    backstory=(
        "You are a legendary tech journalist. You know how to take complex data blocks "
        "and weave them into accessible stories while maintaining perfect professional technical accuracy."
    ),
    tools=[],  # No tools needed; this agent relies strictly on what the researcher finds
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)



# 3. TASK DEFINITIONS (The Work Statements)


# TASK 1: Deep Web Research Assignment
research_task = Task(
    description=(
        "Thoroughly analyze and search the live web for the following topic: '{target_topic}'. "
        "Identify the top 3 critical advancements, relevant statistics, and real-world examples."
    ),
    expected_output="A raw, detailed bullet-point intelligence report containing data facts and source references.",
    agent=researcher_agent  # Linked directly to our search agent
)

# TASK 2: High-Quality Content Synthesis Assignment
writing_task = Task(
    description=(
        "Review the raw intelligence report gathered by the Senior Research Analyst. "
        "Transform those notes into a beautiful, publication-ready article. "
        "Ensure it features an eye-catching title, executive summaries, and clear headers."
    ),
    expected_output="A beautifully styled, publication-ready article written strictly in Markdown formatting.",
    output_file="final_blog_post.md",  # CrewAI will automatically generate this file for you!
    agent=writer_agent  # Linked directly to our writer agent
)


# 4. CREW ORCHESTRATION & KICKOFF


# Grouping the agents and tasks into a sequential workflow crew manager

content_generation_crew = Crew(
    agents=[researcher_agent, writer_agent],
    tasks=[research_task, writing_task],
    process=Process.sequential  # Task 1 must complete before Task 2 begins!
)

def run_my_crew(topic): # Creating the input dictionary required by the research task.
                            
    input_variables = {
        "target_topic": topic  # The key 'target_topic' replaces the placeholder used inside the task description
    }
    # Triggering the CrewAI execution pipeline where:
    # Task 1: The Research Analyst collects real-time web intelligence.
    # Task 2: The Technical Content Writer transforms the research into a structured Markdown article.
    return content_generation_crew.kickoff(inputs=input_variables)
     # Returning the final generated content back to the Gradio user interface.


if __name__ == "__main__":
    print("Initializing Agentic Workflow Crew...")
    
    # Defining the input parameter variable topic whwere we want the agents to research
    input_variables = {
        "target_topic": "AI Agent Framework trends and developments in 2026"
    }
    
    # Running the engine
    result = content_generation_crew.kickoff(inputs=input_variables)
    
    print("\n ==================================================")
    print("REW EXECUTION COMPLETE!")
    print("====================================================\n")
    print(f" final file 'final_blog_post.md' has been generated in the folder.")
