# Agentic Proposal System

An AI-powered system for generating professional project proposals using multiple specialized agents. The system uses Microsoft's Autogen framework to create an interactive multi-agent system that can gather requirements, generate proposals, and handle revisions.

## Features

- Multi-agent system with specialized roles:
  - Requirements Analyst: Gathers and clarifies project requirements
  - Proposal Writer: Creates professional proposal documents
  - Proposal Reviewer: Reviews and suggests improvements
- Automated document generation using branded templates
- Interactive requirement gathering
- Comprehensive proposal sections including:
  - Executive summary
  - Customer requirements
  - Scope statements
  - Solution summary with diagrams
  - Deliverables
  - Cost breakdown
  - RAID analysis
  - Effort estimates
- Support for document revision and feedback

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. The system will start an interactive session where:
   - The Requirements Analyst will gather project information
   - The Proposal Writer will generate the document
   - The Proposal Reviewer will review and suggest improvements

3. You can provide feedback at any point, and the system will revise the proposal accordingly.

## Customization

### Templates
Place your branded Word templates in the `templates` directory. Update the template path in the code when initializing the `ProposalDocumentGenerator`.

### Agent Configurations
Modify the agent configurations in `main.py` to adjust:
- Temperature settings
- System messages
- Model selection
- Maximum conversation rounds

## Requirements

- Python 3.8+
- OpenAI API key
- Microsoft Word (for viewing generated documents)
- Graphviz (for generating diagrams)

## Directory Structure

```
agentic_proposal_system/
├── main.py                 # Main script with agent definitions
├── utils/
│   └── document_generator.py  # Document generation utilities
├── templates/              # Word document templates
├── workspace/             # Working directory for generated files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

Feel free to submit issues and enhancement requests! 