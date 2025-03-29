# Software Agents: Automated Software Development Team

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An automated multi-agent system built using CrewAI that simulates a software development team to solve coding problems. This project demonstrates the power of collaborative AI agents for tackling software development tasks.

## 🌟 Features

* **Multi-Agent Collaboration:** Utilizes CrewAI framework for seamless interaction between specialized agents
* **Automated Problem Analysis:** Research Analyst agent thoroughly analyzes problems
* **Automated Code Generation:** Python Developer agent writes efficient solutions
* **Automated Testing:** Test Engineer agent creates and runs comprehensive test cases
* **Comprehensive Logging:** Detailed execution logs for debugging and monitoring
* **Environment Variable Management:** Secure handling of configuration and API keys
* **Problem Management:** Organized structure for managing unsolved and solved problems

## 🛠️ Tech Stack

* **Framework:** CrewAI
* **Language:** Python 3.8+
* **LLM Integration:** LangChain with ChatOpenAI wrapper
* **Environment Management:** python-dotenv
* **Search Integration:** DuckDuckGo for web research

## 📋 Prerequisites

Before you begin, ensure you have:
* Python 3.8 or higher installed
* OpenAI API key (for GPT-4 access)
* Git (optional, for cloning the repository)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hanuytayal/Software-Agents.git
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
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   OPENAI_TEMPERATURE=0.7
   ```

## 💻 Usage

1. **Add Problems:**
   Place your coding problems in the `problems/unsolved` directory as text files.

2. **Run the Script:**
   ```bash
   python main.py
   ```

3. **Review the Results:**
   - Solutions will be saved in `problems/solved` directory
   - Each solution includes:
     - Original problem description
     - Generated code solution
     - Test cases and results
   - Check `problem_solver.log` for detailed execution information

## 🔍 Project Structure

```
Software-Agents/
├── main.py           # Main script orchestrating the agents
├── agents.py         # Agent definitions and configurations
├── tasks.py          # Task definitions for the agents
├── custom_task.py    # Custom task implementation
├── problems/         # Problem management
│   ├── unsolved/    # Problems to be solved
│   └── solved/      # Solutions and results
├── requirements.txt  # Project dependencies
├── .env.example     # Example environment configuration
└── README.md        # This file
```

## 🤖 Agent Roles

1. **Research Analyst:**
   - Analyzes problem requirements and constraints
   - Identifies edge cases and potential challenges
   - Provides comprehensive problem breakdown

2. **Python Developer:**
   - Writes clean, efficient, and well-documented code
   - Implements solutions following best practices
   - Handles error cases appropriately

3. **Test Engineer:**
   - Creates comprehensive test cases
   - Validates code against requirements
   - Tests edge cases and error conditions
   - Provides detailed test results

## 🔄 Workflow

1. The Research Analyst analyzes the problem and provides a detailed breakdown
2. The Python Developer writes the solution based on the analysis
3. The Test Engineer creates and runs test cases
4. Results are saved with the original problem, solution, and test outcomes

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