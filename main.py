import autogen
from typing import Dict, List
import os
import getpass
import sys
from dotenv import load_dotenv
import re
import time

def validate_api_key(api_key: str) -> bool:
    """Validate the format of the API key"""
    api_key = api_key.strip()
    if not api_key:
        return False
    return True

def setup_api_key():
    """Set up the OpenAI API key from .env file or prompt"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and validate_api_key(api_key):
        print("API key loaded from .env file")
        return api_key
        
    print("\nNo valid API key found in .env file.")
    print("Enter your OpenAI API key (input will be hidden):")
    api_key = getpass.getpass().strip()
    
    if validate_api_key(api_key):
        return api_key
    else:
        print("Invalid API key")
        sys.exit(1)

def create_agents(config_list):
    """Create the agent team"""
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="A human user who needs a project proposal document.",
        human_input_mode="ALWAYS",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "workspace",
            "use_docker": False
        },
    )

    requirements_analyst = autogen.AssistantAgent(
        name="Requirements_Analyst",
        llm_config={
            "config_list": config_list,
            "temperature": 0.7,
        },
        system_message="""You are a senior requirements analyst focusing on one section at a time.
        Gather detailed information about the current section before moving to the next.
        Ask specific, focused questions about the section being discussed."""
    )

    proposal_writer = autogen.AssistantAgent(
        name="Proposal_Writer",
        llm_config={
            "config_list": config_list,
            "temperature": 0.4,
        },
        system_message="""You are an expert proposal writer focusing on one section at a time.
        Write detailed, professional content for the current section.
        Use clear language and proper formatting."""
    )

    proposal_reviewer = autogen.AssistantAgent(
        name="Proposal_Reviewer",
        llm_config={
            "config_list": config_list,
            "temperature": 0.3,
        },
        system_message="""You are a critical proposal reviewer focusing on one section at a time.
        Review the current section for completeness, accuracy, and clarity.
        Suggest specific improvements."""
    )

    return user_proxy, requirements_analyst, proposal_writer, proposal_reviewer

def work_on_section(manager, user_proxy, section_name: str, section_prompt: str):
    """Work on a specific section of the proposal"""
    print(f"\nWorking on: {section_name}")
    print("-" * 50)
    
    user_proxy.initiate_chat(
        manager,
        message=f"""Let's focus on the {section_name} section of the chatbot proposal.
        
        {section_prompt}
        
        Please gather requirements and create content for this section only."""
    )

def main():
    # Set up API key
    api_key = setup_api_key()
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Configure agents
    config_list = [
        {
            "model": "gpt-4-turbo-preview",
            "api_key": api_key,
        }
    ]
    
    # Create agents
    user_proxy, requirements_analyst, proposal_writer, proposal_reviewer = create_agents(config_list)
    
    # Create group chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, requirements_analyst, proposal_writer, proposal_reviewer],
        messages=[],
        max_round=10  # Limit rounds per section to avoid rate limits
    )
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list}
    )
    
    # Work on each section
    sections = {
        "Requirements Gathering": """
        Focus on gathering specific details about:
        1. Existing CRM system and integration requirements
        2. Expected user volume and scalability needs
        3. Security and compliance requirements
        4. Budget constraints
        5. Timeline requirements
        """,
        
        "Technical Solution": """
        Design the technical solution including:
        1. Technology stack selection
        2. Integration architecture
        3. Scalability design
        4. Security measures
        """,
        
        "Implementation Plan": """
        Create a detailed implementation plan including:
        1. Timeline and milestones
        2. Resource requirements
        3. Risk mitigation strategies
        4. Success metrics
        """
    }
    
    try:
        for section_name, section_prompt in sections.items():
            work_on_section(manager, user_proxy, section_name, section_prompt)
            print("\nWaiting 10 seconds before next section to avoid rate limits...")
            time.sleep(10)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 