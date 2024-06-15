from crewai import Agent
class Agents:
    def developer(self):
        return Agent(
            name="Developer",
            description="A software developer who can write software code based on the tasks provided.",
            role="Developer",
            goal="Develop high-quality software solutions.",
            backstory="Has extensive experience in Python and FastAPI development.",
            developer=True,
            tester=False
        )

    def tester(self):
        return Agent(
            name="Tester",
            description="A software tester who can test the software code written based on the tasks provided and double checks rewritten code before it is run for testing. Then compares the results to the expected output, providing a critical analysis of the results.",
            role="Tester",
            goal="Ensure software quality and reliability through thorough testing.",
            backstory="Has extensive experience in software testing and quality assurance.",
            developer=False,
            tester=True
        )
