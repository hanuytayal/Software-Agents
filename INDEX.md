# Codebase Index

## 📁 Project Structure

```
Software-Agents/
├── main.py           # Main orchestration script
├── agents.py         # Agent definitions and configurations
├── tasks.py          # Task definitions for the agents
├── requirements.txt  # Project dependencies
├── .env.example     # Example environment configuration
├── .gitignore       # Git ignore rules
├── LICENSE          # MIT License
├── README.md        # Project documentation
├── INDEX.md         # This file (codebase index)
└── questions.txt    # Problem definitions
```

## 📄 File Descriptions

### Core Files

#### `main.py`
- **Purpose**: Main orchestration script that initializes and runs the CrewAI crew
- **Key Components**:
  - Environment setup and logging configuration
  - Problem definition (QUESTION, EXAMPLE, CONSTRAINTS)
  - Agent and task initialization
  - Crew execution and result handling
- **Dependencies**:
  - crewai
  - python-dotenv
  - logging (standard library)

#### `agents.py`
- **Purpose**: Defines and configures CrewAI agents for software development tasks
- **Key Components**:
  - Local LLM configuration (LM Studio integration)
  - Developer agent definition
  - Tester agent definition
- **Dependencies**:
  - crewai
  - langchain_openai
  - logging (standard library)

#### `tasks.py`
- **Purpose**: Defines tasks for CrewAI agents related to problem analysis and solution generation
- **Key Components**:
  - break_down_task: Analyzes and breaks down problems
  - write_answer_for_tasks: Generates code solutions
  - test_cases: Creates test cases
- **Dependencies**:
  - crewai
  - textwrap (standard library)
  - logging (standard library)

### Configuration Files

#### `requirements.txt`
- **Purpose**: Lists project dependencies and their versions
- **Contents**:
  - crewai>=0.11.0
  - python-dotenv>=1.0.0
  - langchain-openai>=0.0.5

#### `.env.example`
- **Purpose**: Template for environment variable configuration
- **Contents**:
  - OPENAI_API_KEY
  - OPENAI_BASE_URL

#### `.gitignore`
- **Purpose**: Specifies files and directories to be ignored by Git
- **Contents**:
  - Environment files (.env)
  - Python cache files
  - Database files
  - OS-specific files

### Documentation Files

#### `README.md`
- **Purpose**: Main project documentation
- **Contents**:
  - Project overview
  - Features
  - Installation instructions
  - Usage guide
  - Project structure
  - Contributing guidelines

#### `LICENSE`
- **Purpose**: MIT License for the project
- **Type**: MIT License

### Data Files

#### `questions.txt`
- **Purpose**: Stores problem definitions and examples
- **Format**: Text file with problem descriptions, examples, and constraints

## 🔄 Code Flow

1. **Initialization**:
   - `main.py` loads environment variables and sets up logging
   - Initializes agents and tasks using `agents.py` and `tasks.py`

2. **Problem Definition**:
   - Problem details are defined in `main.py` (QUESTION, EXAMPLE, CONSTRAINTS)
   - Can be modified or loaded from `questions.txt`

3. **Agent Execution**:
   - Developer agent breaks down the problem
   - Developer agent writes the solution
   - Tester agent creates test cases

4. **Output**:
   - Results are logged and displayed
   - Solutions are saved to timestamped result files

## 🔧 Key Functions

### In `main.py`
- `crew.kickoff()`: Starts the agent execution process
- `logging.basicConfig()`: Sets up logging configuration

### In `agents.py`
- `developer()`: Creates and configures the developer agent
- `tester()`: Creates and configures the tester agent

### In `tasks.py`
- `break_down_task()`: Creates task for problem analysis
- `write_answer_for_tasks()`: Creates task for solution generation
- `test_cases()`: Creates task for test case generation

## 🔐 Environment Variables

Required environment variables:
- `OPENAI_API_KEY`: API key for LLM access (placeholder for LM Studio)
- `OPENAI_BASE_URL`: Base URL for LLM endpoint (default: http://localhost:1234/v1)

## 📝 Logging

The project uses Python's built-in logging module with:
- Log level: DEBUG
- Output: Console
- Format: Standard logging format

## 🔍 Dependencies

### External Libraries
- crewai: Framework for AI agent orchestration
- python-dotenv: Environment variable management
- langchain-openai: LLM integration

### Standard Library
- logging: Logging functionality
- textwrap: Text formatting
- typing: Type hints 