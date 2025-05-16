import os
import openai

# Set your OpenAI API key in environment variable OPENAI_API_KEY before running this script
openai.api_key = os.getenv("OPENAI_API_KEY")

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def generate(self, context):
        prompt = self.create_prompt(context)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes professional proposal content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating content in {self.name}: {e}"

    def create_prompt(self, context):
        raise NotImplementedError("Each agent must implement create_prompt.")

class ExecutiveSummaryAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Write an executive summary for a business proposal about {context['project']} "
            f"for the customer {context['customer']}. The summary should highlight the goals, "
            "importance, and benefits of the project."
        )

class RequirementsAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Create a detailed list of customer requirements for the project {context['project']} "
            f"requested by {context['customer']}. Format as a table with requirement IDs and descriptions."
        )

class ScopeAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Define the in-scope and out-of-scope items clearly for the project titled '{context['project']}'. "
            "Use bullet points under 'In Scope' and 'Out of Scope' headings."
        )

class SolutionSummaryAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Provide a high-level solution summary for the project {context['project']}. "
            "Include key activities, integration points, and main architectural considerations."
        )

class DeliverablesAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"List the key deliverables for the project {context['project']} in bullet point format."
        )

class CostsAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Generate a sample resource cost table and mention any licensing requirements "
            f"for the project {context['project']}. Format the table with columns: Activity, Role, Type, Quantity (Days), Unit Cost, Total Cost."
        )

class RAIDAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Describe the risks, assumptions, issues, and dependencies (RAID) for the project {context['project']}."
        )

class TaskBreakdownAgent(BaseAgent):
    def create_prompt(self, context):
        return (
            f"Provide a task breakdown with estimated effort (in days) for the project {context['project']}. "
            "Include tasks such as requirements gathering, architecture & design, system setup, testing, documentation, and training."
        )

class ProposalOrchestrator:
    def __init__(self, context):
        self.context = context
        self.agents = {
            "Executive Summary": ExecutiveSummaryAgent("Executive Summary Agent"),
            "Customer Requirements": RequirementsAgent("Requirements Agent"),
            "Scope Statement": ScopeAgent("Scope Agent"),
            "Solution Summary": SolutionSummaryAgent("Solution Summary Agent"),
            "Deliverables": DeliverablesAgent("Deliverables Agent"),
            "Costs": CostsAgent("Costs Agent"),
            "RAID": RAIDAgent("RAID Agent"),
            "Task Breakdown and Effort Estimates": TaskBreakdownAgent("Task Breakdown Agent"),
        }

    def generate_proposal(self):
        proposal_content = {}
        for section, agent in self.agents.items():
            print(f"Generating section: {section}...")
            content = agent.generate(self.context)
            proposal_content[section] = content
        return proposal_content


if __name__ == "__main__":
    context = {
        "customer": "ACME Corp",
        "project": "ZTNA Functionality for Fiori Web Browser"
    }
    orchestrator = ProposalOrchestrator(context)
    proposal = orchestrator.generate_proposal()

    print("\n\n======= GENERATED PROPOSAL =======\n")
    for section, content in proposal.items():
        print(f"--- {section} ---\n{content}\n{'='*60}\n")
