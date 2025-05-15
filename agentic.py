from autogen import AssistantAgent, UserProxyAgent
import os

# Load design standards and sample template
with open("sample_proposal.txt", "r") as f:
    sample_proposal = f.read()

with open("design_standards.md", "r") as f:
    design_standards = f.read()

def generate_proposal(requirements):
    llm_config = {
        "config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}],
        "timeout": 180,
    }

    # Step 1: Ask for clarifications
    question_agent = AssistantAgent(
        name="ScopeClarifier",
        llm_config=llm_config,
        system_message="You're a consultant. Ask the client for missing project details like in-scope features, deliverables, constraints, and priorities. Ask no more than 5 questions."
    )

    # Step 2: Analyze cost assumptions
    estimator_agent = AssistantAgent(
        name="CostValidator",
        llm_config=llm_config,
        system_message="You're a cost analyst. Identify any cost estimates in the proposal and check if they're reasonable. If not, correct them."
    )

    # Step 3: Final proposal writer
    writer_agent = AssistantAgent(
        name="ProposalWriter",
        llm_config=llm_config,
        system_message=(
            "You are a proposal writer. Use the following design standards:\n\n"
            f"{design_standards}\n\n"
            "and follow the structure from this template:\n\n"
            f"{sample_proposal}\n\n"
            "Incorporate answers from the client and cost corrections to generate the final proposal."
        )
    )

    # User proxy
    user_proxy = UserProxyAgent(name="Client", human_input_mode="ALWAYS")

    # Phase 1 - Clarify
    user_proxy.initiate_chat(question_agent, message=f"Client brief:\n{requirements}")

    # Phase 2 - Cost sanity check
    user_proxy.initiate_chat(estimator_agent, message="Here is the draft proposal. Please check the cost estimates for accuracy.")

    # Phase 3 - Final generation
    user_proxy.initiate_chat(writer_agent, message="Generate the full final proposal incorporating everything.")

    return user_proxy.last_message()["content"]
