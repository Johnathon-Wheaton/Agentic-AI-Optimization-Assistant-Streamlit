# AI-Powered Optimization Assistant

Introducing a consulting team of AI agents here to solve your optimization problems. This application was designed for business users who have an optimization problem but don't have the technical expertise to solve it on their own. This interactive Streamlit application ([available here](https://agentic-ai-optimization-assistant.streamlit.app/)) uses AI agents to help solve optimization problems through natural conversation.

A consultant agent converses with the user, asking clarifying and probing questions to ensure it understand all details about the problem. Then, the consultant works in the backend with a team of agents to formulate, code, run, (and fix, rerun as needed), and output the results of the optimization model.

## Features

- Natural language interface for describing optimization problems
- Multi-agent system with specialized roles:
  - Consultant: Helps understand and formulate the problem
  - Coder: Implements the optimization model
  - Code Critic: Reviews and validates the implementation
  - Checker: Verifies the solution and outputs results
- Automatic Excel output generation with solution details
- Support for linear programming problems using PuLP
- Interactive chat interface with real-time updates
- Configurable OpenAI model selection

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (see Installation section)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Johnathon-Wheaton/Agentic-AI-Optimization-Assistant-Streamlit.git
cd Agentic-AI-Optimization-Assistant-Streamlit
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, you'll need:

1. An OpenAI API key
2. Selection of preferred OpenAI model (gpt-3.5-turbo or gpt-4-mini)
3. Optional: Adjustment of maximum conversation rounds (default: 40)

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. In the sidebar:
   - Enter your OpenAI API key
   - Select your preferred model
   - Adjust the maximum rounds if needed

3. Interact with the consultant to describe your optimization problem:
   - Provide detailed information about your problem
   - Answer the consultant's questions
   - Review the problem formulation

4. Wait for the AI team to solve your problem:
   - The system will automatically handle model implementation
   - Code review and validation will be performed
   - Results will be verified

5. Download Results:
   - Once solved, an Excel file will be generated
   - Click the download button to save your results
   - The Excel file includes multiple sheets with detailed solution information

## System Architecture

The application uses a multi-agent system with the following components:

- **Consultant Agent**: Interfaces with users to understand requirements
- **Coder Agent**: Implements optimization models in Python
- **Code Critic Agent**: Reviews implementation for accuracy
- **Checker Agent**: Validates solutions and generates output
- **Group Chat Manager**: Coordinates agent interactions
- **User Proxy Agent**: Handles user interactions and code execution

## Output Format

The solution is provided in an Excel file with multiple sheets:

- Summary sheet with top-level results
- Detailed sheets for complex data structures
- Variable values and optimization results

## Limitations

- Maximum conversation rounds: 40 by default
- Requires stable internet connection for API calls
- Solution time depends on problem complexity and chosen model

## Troubleshooting

Common issues and solutions:

1. If the solution times out:
   - Increase the maximum rounds in the sidebar
   - Try simplifying the problem
   - Check if the problem is well-formed

2. If the model is infeasible:
   - Verify input constraints
   - Check for conflicting requirements
   - Work with the consultant to reformulate the problem

3. If API errors occur:
   - Verify your API key
   - Check your internet connection
   - Ensure you have sufficient API credits

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [AutoGen](https://github.com/microsoft/autogen) for AI agents
- Powered by OpenAI's language models