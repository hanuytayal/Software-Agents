# tasks.py
"""
Defines tasks for CrewAI agents related to analyzing a LeetCode problem,
generating a solution, and creating test cases.
"""

import logging
from textwrap import dedent
from crewai import Agent
from typing import List
from custom_task import CustomTask

# Get a logger instance for this module
logger = logging.getLogger(__name__)

class Tasks:
    """
    A container class for methods that generate specific CrewAI Task objects
    for solving coding problems.
    """
    def break_down_task(self, agent: Agent, question: str, example: str, constraints: str) -> CustomTask:
        """
        Creates a task for an agent to analyze and break down a given LeetCode problem
        into actionable development steps.

        Args:
            agent: The CrewAI agent assigned to this task.
            question (str): The main problem description.
            example (str): Examples illustrating the problem.
            constraints (str): Constraints on the input/output.

        Returns:
            A CustomTask object for breaking down the problem.
        """
        logger.debug(f"Creating task 'break_down_task' for agent {agent.role}")
        return CustomTask(
            description=dedent(f"""\
                Analyze the provided LeetCode problem:
                Question: "{question}"
                Examples: "{example}"
                Constraints: "{constraints}"

                Deeply understand the requirements, examples, and constraints.
                Break down the problem into a clear, sequential list of
                software development tasks required to create a working solution.
            """),
            expected_output=dedent("""\
                A comprehensive list of clear and executable software development tasks
                that can be directly used by a developer to write the code solution.
                The list should be ordered logically for implementation.
            """),
            agent=agent
        )

    def write_answer_for_tasks(self, agent: Agent, context: List[CustomTask]) -> CustomTask:
        """
        Creates a task for an agent to write the code solution based on
        the previously defined development tasks.

        Args:
            agent: The CrewAI agent assigned to this task.
            context (List[CustomTask]): A list of prerequisite tasks, expected to include
                                   the output of 'break_down_task'.

        Returns:
            A CustomTask object for writing the code solution.
        """
        logger.debug(f"Creating task 'write_answer_for_tasks' for agent {agent.role}")
        return CustomTask(
            description=dedent(f"""\
                Based on the provided breakdown of software development tasks,
                write the actual software code that solves the original LeetCode problem.
                Ensure the code is well-commented, follows best practices, and correctly
                implements the logic required by the problem description and examples.
            """),
            expected_output=dedent("""\
                A complete, correct, and well-documented code solution (e.g., in Python)
                that solves the specified LeetCode problem, adhering to the logic
                derived from the problem breakdown. The code should be ready for testing.
            """),
            agent=agent,
            context=context
        )

    def test_cases(self, agent: Agent, context: List[CustomTask]) -> CustomTask:
        """
        Creates a task for an agent to generate test cases for the developed code solution.

        Args:
            agent: The CrewAI agent assigned to this task.
            context (List[CustomTask]): A list of prerequisite tasks, expected to include
                                   the output of 'write_answer_for_tasks'.

        Returns:
            A CustomTask object for generating test cases.
        """
        logger.debug(f"Creating task 'test_cases' for agent {agent.role}")
        return CustomTask(
            description=dedent(f"""\
                Based on the original LeetCode problem description, examples, constraints,
                and the provided code solution, create a comprehensive set of test cases.
                Include edge cases, base cases, and cases derived from the examples
                and constraints.
            """),
            expected_output=dedent("""\
                A comprehensive set of test cases (e.g., input/output pairs or a test script)
                that thoroughly validate the functionality, correctness, and edge case handling
                of the provided software code solution against the original problem requirements.
            """),
            agent=agent,
            context=context
        )