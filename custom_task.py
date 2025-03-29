"""
Custom Task class that extends CrewAI's Task to store output.
"""

from crewai import Task
from typing import Optional

class CustomTask(Task):
    """
    A custom Task class that extends CrewAI's Task to store the output
    of task execution.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output: Optional[str] = None

    def set_output(self, output: str) -> None:
        """
        Sets the output of the task execution.

        Args:
            output (str): The output from task execution.
        """
        self.output = output

    def get_output(self) -> Optional[str]:
        """
        Gets the output of the task execution.

        Returns:
            Optional[str]: The output from task execution, if available.
        """
        return self.output 