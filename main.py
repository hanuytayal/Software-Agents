# main.py
import logging
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew
from tasks import Tasks
from agents import Agents

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

tasks = Tasks()
agents = Agents()

# Create a Crew object
# Grab Question from input
question = """Question: Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
'.' Matches any single character.
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial)."""

# Grab Example from input
example = """Example 1:
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

# Grab Constraints from input
constraints = """Constraints:
1 <= s.length <= 20
1 <= p.length <= 20
s contains only lowercase English letters.
p contains only lowercase English letters, '.', and '*'.
It is guaranteed for each appearance of the character '*', there will be a previous valid character to match."""

# Create Agents
developer = agents.developer()
tester = agents.tester()

# Assign tasks to agents
logging.debug("Assigning tasks to developer")
break_down_task = tasks.break_down_task(developer, question, example, constraints)
logging.debug("Developer task: Break down the problem")

write_answer_for_tasks = tasks.write_answer_for_tasks(developer, break_down_task)
logging.debug("Developer task: Write answer for tasks")

logging.debug("Assigning tasks to tester")
test_cases = tasks.test_cases(tester, write_answer_for_tasks)
logging.debug("Tester task: Create test cases")

# Initialize the Crew with agents and tasks
crew = Crew(
    agents=[developer, tester],
    tasks=[break_down_task,
           write_answer_for_tasks,
           test_cases]
)

# Start the crew and run the tasks
logging.debug("Starting the crew")
result = crew.kickoff()

# Print the result
logging.debug("Result from the crew")
print(result)
