import gradio as gr

from app import run_my_crew  

def chat_with_agents(user_message, history):
    """
    This wrapper function takes the text from the Gradio input box,
    sends it to your CrewAI agents, catches any crashes, and returns the output text.
    """
    try:
        
        agent_response = run_my_crew(user_message)
        return str(agent_response)
        
    except Exception as e:

        return f"System Error: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_with_agents,
    title="Multi-Agent Worker System",
    description="Type your prompt below to kickoff the CrewAI agent workspace."
)
demo.launch()
