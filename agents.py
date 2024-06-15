import logging
from crewai import Agent
from openai import OpenAI

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the LLaMA 3 client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class IntelligentAgent(Agent):
    def __init__(self, name, description, role, goal, backstory, developer=False, tester=False, client=None, history=None):
        # Call the parent class (Agent) initializer
        super().__init__(name=name, description=description, role=role, goal=goal, backstory=backstory, developer=developer, tester=tester)
        
        # Log the initialization of the agent
        # logging.debug(f"Initialized {self.role}: {self.name}")

    def chat(self, user_input):
        # Log the user input
        logging.debug(f"User input: {user_input}")
        
        # Append the user input to the history
        self.history.append({"role": "user", "content": user_input})

        # Call the LLaMA 3 model to get a completion
        completion = self.client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=self.history,
            temperature=0.7,
            stream=True,
        )

        # Initialize a new message from the assistant
        new_message = {"role": "assistant", "content": ""}
        logging.debug("Receiving response from LLaMA 3 model")

        # Process the completion chunks
        for chunk in completion:
            if 'delta' in chunk.choices[0]:
                if 'content' in chunk.choices[0].delta:
                    logging.debug(f"Received chunk: {chunk.choices[0].delta.content}")
                    new_message["content"] += chunk.choices[0].delta.content

        # Append the assistant's response to the history
        self.history.append(new_message)
        
        # Log the assistant's response
        logging.debug(f"Assistant response: {new_message['content']}")
        return new_message["content"]

class Agents:
    def developer(self):
        # Create and return a developer agent
        return IntelligentAgent(
            name="Developer",
            description="A software developer who can write software code based on the tasks provided.",
            role="Developer",
            goal="Develop high-quality software solutions.",
            backstory="You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful.",
            client=client,
            history=[],
            developer=True,
            tester=False
        )

    def tester(self):
        # Create and return a tester agent
        return IntelligentAgent(
            name="Tester",
            description="A software tester who can test the software code written based on the tasks provided and double-check rewritten code before it is run for testing. Then compares the results to the expected output, providing a critical analysis of the results.",
            role="Tester",
            goal="Ensure software quality and reliability through thorough testing.",
            backstory="Has extensive experience in software testing and quality assurance.",
            developer=False,
            tester=True
        )
