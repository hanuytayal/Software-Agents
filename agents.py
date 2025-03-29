# agents.py
"""
Defines and configures CrewAI agents for software development tasks,
using a local LLM instance (via LM Studio's OpenAI-compatible endpoint).
"""

import logging
from crewai import Agent
# Import ChatOpenAI from langchain_openai to wrap the local LLM endpoint
from langchain_openai import ChatOpenAI

# Get a logger instance for this module
logger = logging.getLogger(__name__)

# --- Local LLM Configuration ---
# Configure the LLM wrapper to connect to your local LM Studio instance
# Ensure LM Studio is running and serving the model on http://localhost:1234
try:
    local_llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio", # Use the placeholder key for LM Studio
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF", # Specify the model being served
        temperature=0.7
    )
    logger.info("Connected to local LLM via LangChain wrapper.")
except Exception as e:
    logger.error(f"Failed to initialize LangChain LLM wrapper: {e}")
    # Handle error appropriately - maybe exit or use a fallback
    local_llm = None # Set to None if connection fails

class Agents:
    """
    A factory class for creating pre-configured CrewAI agents
    using the defined local LLM.
    """
    def developer(self) -> Agent:
        """
        Creates and returns a 'Developer' agent configured for writing code.

        Returns:
            A CrewAI Agent object representing the developer.

        Raises:
            ValueError: If the local LLM failed to initialize.
        """
        if local_llm is None:
            raise ValueError("Local LLM is not available. Cannot create agent.")

        logger.debug("Creating Developer agent")
        return Agent(
            role="Developer",
            goal="Develop high-quality, correct, and well-documented software code based on provided tasks and requirements.",
            backstory=dedent("""\
                You are a skilled software developer focused on implementing solutions
                accurately based on requirements. You write clean, efficient, and
                well-commented code following best practices."""),
            allow_delegation=False, # Developer likely works independently on coding tasks
            verbose=True,
            llm=local_llm # Use the configured local LLM
        )

    def tester(self) -> Agent:
        """
        Creates and returns a 'Tester' agent configured for testing code
        and ensuring quality.

        Returns:
            A CrewAI Agent object representing the tester.

        Raises:
            ValueError: If the local LLM failed to initialize.
        """
        if local_llm is None:
            raise ValueError("Local LLM is not available. Cannot create agent.")

        logger.debug("Creating Tester agent")
        return Agent(
            role="Tester",
            goal="Ensure software quality and reliability by creating comprehensive test cases and verifying code correctness against requirements.",
            backstory=dedent("""\
                You are a meticulous Quality Assurance expert with extensive experience
                in software testing. You excel at identifying edge cases, creating
                thorough test plans, and critically analyzing code behavior against
                expected outcomes."""),
            allow_delegation=False, # Tester likely works independently
            verbose=True,
            llm=local_llm # Use the configured local LLM
        )

# Helper function (optional) to make importing easier
# You can directly instantiate Agents() in main.py as well
# def get_agents_factory():
#     return Agents()