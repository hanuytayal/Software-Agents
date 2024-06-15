#Tasks given to each worker
from textwrap import dedent
from crewai import Task

class Tasks:
    def break_down_task(self, agent, question, example, constrains):
        return Task(
                            description=dedent(f"""\
                                    Analyze the provided LeetCode problem "{question}". Focus on deeply understanding the examples provided here "{example}". Also, carefully review the constrains here "{constrains}". Use this information to breakdown the problem into tasks which will be then used to write software code. Compile a list of these tasks.
                              """),
                            expected_output=dedent("""\
                                    A comprehensive list of clear and executable software development tasks that can be given to a software developer to write software code ."""),
                            agent=agent
                    )
    # def write_answer_for_tasks(self, agent, task):
    #                 return Task(
    #                         description=dedent(f"""\
    #                                 Write a detailed answer to the following question:
    #                                 {task.description}"""),
    #                         expected_output=dedent("""\
    #                                 A well-structured report that effectively summarizes the company's key aspects and provides actionable insights on leveraging these in a job posting."""),
    #                         agent=agent
    #                 )
    #