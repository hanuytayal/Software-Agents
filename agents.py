# agents.py
"""
Defines and configures CrewAI agents for software development tasks,
using OpenAI's GPT models.
"""

import logging
import os
from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI

# Get a logger instance for this module
logger = logging.getLogger(__name__)

# --- OpenAI Configuration ---
try:
    # Log environment variables
    logger.debug(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")
    logger.debug(f"OPENAI_TEMPERATURE: {os.getenv('OPENAI_TEMPERATURE')}")

    # Configure OpenAI LLM
    openai_llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    logger.info("Connected to OpenAI LLM via LangChain wrapper.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI LLM wrapper: {str(e)}")
    logger.error(f"Error type: {type(e)}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    # Handle error appropriately - maybe exit or use a fallback
    openai_llm = None # Set to None if connection fails

class Agents:
    """
    A factory class for creating pre-configured CrewAI agents
    using OpenAI's GPT models.
    """
    def developer(self) -> Agent:
        """
        Creates and returns a 'Developer' agent configured for writing code.

        Returns:
            A CrewAI Agent object representing the developer.

        Raises:
            ValueError: If the OpenAI LLM failed to initialize.
        """
        if openai_llm is None:
            raise ValueError("OpenAI LLM is not available. Cannot create agent.")

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
            llm=openai_llm # Use the configured OpenAI LLM
        )

    def tester(self) -> Agent:
        """
        Creates and returns a 'Tester' agent configured for testing code
        and ensuring quality.

        Returns:
            A CrewAI Agent object representing the tester.

        Raises:
            ValueError: If the OpenAI LLM failed to initialize.
        """
        if openai_llm is None:
            raise ValueError("OpenAI LLM is not available. Cannot create agent.")

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
            llm=openai_llm # Use the configured OpenAI LLM
        )

# Helper function (optional) to make importing easier
# You can directly instantiate Agents() in main.py as well
# def get_agents_factory():
#     return Agents()