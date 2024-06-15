#Launch
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew

from tasks import Tasks
from agents import Agents


tasks = Tasks()
agents = Agents()

#Create a Crew object
#Grab Question from input
question = input("Enter the question: ")

#Grab Example from input
example = input("Enter the example: ")

#Grab Constrains from input
constrains = input("Enter the constrains: ")

#Grab answers to compare results  from input
answers = input("Enter the answers: ")

#Create Agents


#Assign tasks to agents


#Run the agents with sequential execution

#Start the agents

#Print the results