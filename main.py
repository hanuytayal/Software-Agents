# main.py
"""
Initializes and runs a CrewAI crew with a developer and tester agent
to solve a regular expression matching problem.

This script defines the problem (question, example, constraints),
creates the necessary agents (developer, tester) and tasks
(break down problem, write solution, create test cases),
and then kicks off the crew to execute the tasks sequentially.
"""

import logging
from dotenv import load_dotenv
from crewai import Crew
from tasks import Tasks # Assuming tasks.py contains the Tasks class definition
from agents import Agents # Assuming agents.py contains the Agents class definition

# --- Setup ---
# Load environment variables (e.g., API keys for CrewAI agents)
load_dotenv()

# Initialize logging - DEBUG level provides detailed execution information
logging.basicConfig(level=logging.DEBUG)

# --- Problem Definition ---
# Define the core question/problem for the crew to solve
QUESTION = """Question: Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
'.' Matches any single character.
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial)."""

# Provide examples to clarify the expected behavior
EXAMPLE = """Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)"."""

# Specify the constraints for the input strings
CONSTRAINTS = """Constraints:
1 <= s.length <= 20
1 <= p.length <= 20
s contains only lowercase English letters.
p contains only lowercase English letters, '.', and '*'.
It is guaranteed for each appearance of the character '*', there will be a previous valid character to match."""

# --- Agent and Task Initialization ---
logging.debug("Initializing agents and tasks...")
try:
    tasks_manager = Tasks()
    agents_manager = Agents()

    # Create Agents
    developer = agents_manager.developer()
    tester = agents_manager.tester()
    logging.debug("Agents created successfully.")

    # Define Tasks for the agents
    # Task 1: Developer breaks down the problem based on the definition
    break_down_task = tasks_manager.break_down_task(
        agent=developer,
        question=QUESTION,
        example=EXAMPLE,
        constraints=CONSTRAINTS
    )
    logging.debug("Task created: break_down_task")

    # Task 2: Developer writes the solution based on the breakdown
    # This task depends on the output of break_down_task
    write_answer_for_tasks = tasks_manager.write_answer_for_tasks(
        agent=developer,
        context=[break_down_task] # Pass as a list
    )
    logging.debug("Task created: write_answer_for_tasks")

    # Task 3: Tester creates test cases based on the developer's answer
    # This task depends on the output of write_answer_for_tasks
    test_cases = tasks_manager.test_cases(
        agent=tester,
        context=[write_answer_for_tasks] # Pass as a list
    )
    logging.debug("Task created: test_cases")

except Exception as e:
    logging.error(f"Error during agent or task initialization: {e}")
    # Optionally exit or handle the error appropriately
    exit(1)


# --- Crew Execution ---
logging.debug("Initializing the Crew...")
# Initialize the Crew with the defined agents and the sequence of tasks
crew = Crew(
    agents=[developer, tester],
    tasks=[
        break_down_task,
        write_answer_for_tasks,
        test_cases
        ],
    verbose=True  # Changed from 2 to True for proper boolean value
)

# Start the crew's task execution
logging.debug("Starting the crew kickoff...")
try:
    result = crew.kickoff()

    # Print the final result from the crew's execution
    logging.debug("Crew execution finished. Final Result:")
    print("\n--- Final Result ---")
    print(result)
    print("--------------------")

except Exception as e:
    logging.error(f"Error during crew execution: {e}")

logging.debug("Script finished.")