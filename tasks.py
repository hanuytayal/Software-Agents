# tasks.py
import logging
from textwrap import dedent
from crewai import Task

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

class Tasks:
    def break_down_task(self, agent, question, example, constraints):
        logging.debug(f"Creating task to break down the problem: {question}")
        return Task(
            description=dedent(f"""\
                Analyze the provided LeetCode problem "{question}". Focus on deeply understanding the examples provided here "{example}". Also, carefully review the constraints here "{constraints}". Use this information to breakdown the problem into tasks which will be then used to write software code. Compile a list of these tasks.
            """),
            expected_output=dedent("""\
                A comprehensive list of clear and executable software development tasks that can be given to a software developer to write software code.
            """),
            agent=agent
        )

    def write_answer_for_tasks(self, agent, task):
        logging.debug(f"Creating task to write answer: {task.description}")
        return Task(
            description=dedent(f"""\
                Write a detailed answer to the following question:
                {task.description}
            """),
            expected_output=dedent("""\
                A well-structured report that effectively summarizes the company's key aspects and provides actionable insights on leveraging these in a job posting.
            """),
            agent=agent
        )

    # Create test cases and verify the output
    def test_cases(self, agent, task):
        logging.debug(f"Creating task to write test cases: {task.description}")
        return Task(
            description=dedent(f"""\
                Write test cases for the following question:
                {task.description}
            """),
            expected_output=dedent("""\
                A comprehensive set of test cases that thoroughly validate the functionality of the software code written.
            """),
            agent=agent
        )
