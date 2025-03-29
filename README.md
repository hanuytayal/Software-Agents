# Software Agents: Automated Software Development Team

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated multi-agent system built using CrewAI that simulates a software development team to break down problems, write code, and review it. This project demonstrates the power of collaborative AI agents for tackling software development tasks.

## 🌟 Features

* **Multi-Agent Collaboration:** Utilizes CrewAI framework for seamless interaction between specialized agents
* **Automated Task Breakdown:** Manager agent intelligently decomposes complex problems
* **Automated Code Generation:** Engineer agent writes code based on defined tasks
* **Automated Code Review/Testing:** Reviewer agent provides feedback on the generated code
* **Local LLM Integration:** Designed to work with local LLMs via an OpenAI-compatible endpoint (e.g., LM Studio)
* **Comprehensive Logging:** Detailed execution logs for debugging and monitoring
* **Environment Variable Management:** Secure handling of configuration and API keys

## 🛠️ Tech Stack

* **Framework:** CrewAI
* **Language:** Python 3.8+
* **LLM Integration:** LangChain with ChatOpenAI wrapper
* **Local LLM Server:** LM Studio (or any OpenAI-compatible endpoint)
* **Core LLM:** Meta-Llama-3-8B-Instruct-GGUF (via LM Studio)
* **Environment Management:** python-dotenv

## 📋 Prerequisites

Before you begin, ensure you have:
* Python 3.8 or higher installed
* Access to a running LLM (e.g., LM Studio serving a compatible model)
* Git (optional, for cloning the repository)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Software-Agents.git
   cd Software-Agents
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration:
   ```
   # For LM Studio, the API key is typically a placeholder
   OPENAI_API_KEY=lm-studio
   OPENAI_BASE_URL=http://localhost:1234/v1
   ```

## 💻 Usage

1. **Start your LLM Server:**
   - Launch LM Studio
   - Load the Meta-Llama-3-8B-Instruct-GGUF model
   - Start the server on port 1234

2. **Define the Problem:**
   Modify the following variables in `main.py`:
   ```python
   QUESTION = "Your problem description"
   EXAMPLE = "Example inputs and outputs"
   CONSTRAINTS = "Problem constraints"
   ```

3. **Run the Script:**
   ```bash
   python main.py
   ```

4. **Review the Output:**
   - The script will log interactions between agents
   - Final results will be displayed in the console
   - Check the logs for detailed execution information

## 🔍 Project Structure

```
Software-Agents/
├── main.py           # Main script orchestrating the agents
├── agents.py         # Agent definitions and configurations
├── tasks.py          # Task definitions for the agents
├── requirements.txt  # Project dependencies
├── .env.example     # Example environment configuration
└── README.md        # This file
```

## 🤖 Agent Roles

1. **Developer Agent:**
   - Analyzes and breaks down complex problems
   - Writes clean, efficient, and well-documented code
   - Follows best practices and coding standards

2. **Tester Agent:**
   - Creates comprehensive test cases
   - Validates code against requirements
   - Identifies edge cases and potential issues

## 🔄 Workflow

1. The Developer agent analyzes the problem and breaks it down into tasks
2. Based on the breakdown, the Developer writes the solution
3. The Tester agent reviews the code and creates test cases
4. The process is logged and results are presented

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* Built using the awesome [CrewAI](https://github.com/joaomdmoura/crewAI) framework
* Developed during the [AI Tinkerers Seattle](https://www.meetup.com/ai-tinkerers-seattle/) hackathon
* Special thanks to all contributors and the open-source community

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the existing issues
2. Create a new issue with a detailed description
3. Include relevant logs and error messages