"""
CrewAI Problem Solver

This script uses CrewAI to solve coding problems. It processes problems from the problems/unsolved directory
and saves solutions to the problems/solved directory.

Directory Structure:
    problems/
        unsolved/     # Contains problem files to be solved
        solved/       # Contains solved problems and their results

Usage:
    python main.py

The script will:
1. Load all problems from problems/unsolved/
2. Process each problem using CrewAI
3. Save solutions to problems/solved/
4. Move solved problems to problems/solved/
"""

import os
import sys
import re
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from tasks import Tasks  # Import our local Tasks class

# --- Logging Configuration ---
def setup_logging() -> None:
    """Configure logging with a clear format and appropriate level."""
    logging.basicConfig(
        level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('problem_solver.log', encoding='utf-8')
        ]
    )
    logging.info("Logging initialized")

# --- Tool Creation ---
class WebSearchTool(BaseTool):
    """Tool for performing web searches using DuckDuckGo."""
    
    name: str = "web_search"
    description: str = "Useful for searching the web for information about algorithms, data structures, and coding problems."
    search: Optional[DuckDuckGoSearchRun] = None
    
    def __init__(self):
        super().__init__()
        self.search = DuckDuckGoSearchRun()
    
    def _run(self, query: str) -> str:
        """Run the web search with the given query."""
        try:
            return self.search.run(query)
        except Exception as e:
            logging.error(f"Error performing web search: {str(e)}")
            return f"Error performing web search: {str(e)}"

# --- Problem Management ---
class ProblemManager:
    """Manages problem files and directories."""
    
    def __init__(self, unsolved_dir: str = 'problems/unsolved', solved_dir: str = 'problems/solved'):
        """
        Initialize the problem manager.
        
        Args:
            unsolved_dir: Directory containing unsolved problems
            solved_dir: Directory containing solved problems
        """
        self.unsolved_dir = unsolved_dir
        self.solved_dir = solved_dir
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        os.makedirs(self.unsolved_dir, exist_ok=True)
        os.makedirs(self.solved_dir, exist_ok=True)
    
    def get_unsolved_problems(self) -> List[os.DirEntry]:
        """
        Get all unsolved problem files.
        
        Returns:
            List of problem files in the unsolved directory
        """
        return [f for f in os.scandir(self.unsolved_dir) if f.is_file() and f.name.endswith('.txt')]
    
    def mark_as_solved(self, problem_file: os.DirEntry) -> None:
        """
        Move a problem file to the solved directory.
        
        Args:
            problem_file: The problem file to mark as solved
        """
        solved_path = os.path.join(self.solved_dir, problem_file.name)
        os.rename(problem_file.path, solved_path)
        logging.info(f"Moved {problem_file.name} to solved directory")

# --- Results Management ---
class ResultsManager:
    """Manages saving and formatting solution results."""
    
    def __init__(self, solved_dir: str):
        """
        Initialize the results manager.
        
        Args:
            solved_dir: Directory where results will be saved
        """
        self.solved_dir = solved_dir
        os.makedirs(solved_dir, exist_ok=True)
    
    def save_to_file(self, problem_file: os.DirEntry, solution: str, test_cases: List[Dict[str, Any]], test_results: str) -> str:
        """
        Save solution results to a file.
        
        Args:
            problem_file: The original problem file
            solution: The solution code
            test_cases: List of test cases
            test_results: Results of running the tests
            
        Returns:
            Path to the saved results file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        problem_name = os.path.splitext(problem_file.name)[0]
        results_file = os.path.join(self.solved_dir, f"{problem_name}_results_{timestamp}.txt")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write("=== Problem ===\n")
            with open(problem_file.path, 'r', encoding='utf-8') as problem:
                f.write(problem.read())
            f.write("\n\n=== Solution ===\n")
            f.write(solution)
            f.write("\n\n=== Test Cases ===\n")
            for i, test in enumerate(test_cases, 1):
                f.write(f"\nTest Case {i}:\n")
                f.write(f"Input: {test['input']}\n")
                f.write(f"Expected: {test['expected']}\n")
            f.write("\n=== Test Results ===\n")
            f.write(test_results)
        
        logging.info(f"Results saved to: {results_file}")
        return results_file

# --- Problem Processing ---
class ProblemProcessor:
    """Processes individual problems using CrewAI."""
    
    def __init__(self, solved_dir: str = 'problems/solved'):
        """Initialize the problem processor."""
        logging.debug("Initializing ProblemProcessor")
        self.results_manager = ResultsManager(solved_dir)
        try:
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7
            )
            logging.debug("LLM initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize LLM: {str(e)}")
            raise
    
    def process_problem(self, problem_file: os.DirEntry) -> Optional[str]:
        """Process a single problem file."""
        logging.info(f"Starting to process problem: {problem_file.name}")
        try:
            # Read problem definition
            with open(problem_file.path, 'r', encoding='utf-8') as f:
                problem_definition = f.read()
            logging.debug(f"Problem definition loaded, length: {len(problem_definition)}")
            
            # Extract problem components
            question = extract_question(problem_definition)
            examples = extract_examples(problem_definition)
            constraints = extract_constraints(problem_definition)
            
            # Create agents
            logging.debug("Creating agents...")
            researcher = Agent(
                role='Research Analyst',
                goal='Research and analyze the problem thoroughly',
                backstory='Expert in problem analysis and research',
                tools=[WebSearchTool()],
                llm=self.llm
            )
            logging.debug("Research agent created")
            
            coder = Agent(
                role='Python Developer',
                goal='Write efficient and correct Python code',
                backstory='Senior Python developer with expertise in algorithms',
                llm=self.llm
            )
            logging.debug("Coder agent created")
            
            tester = Agent(
                role='Test Engineer',
                goal='Create comprehensive test cases',
                backstory='Expert in software testing and quality assurance',
                llm=self.llm
            )
            logging.debug("Tester agent created")
            
            # Create tasks using the Tasks class
            tasks = Tasks()
            research_task = tasks.break_down_task(researcher, question, examples, constraints)
            coding_task = tasks.write_answer_for_tasks(coder, [research_task])
            testing_task = tasks.test_cases(tester, [coding_task])
            
            # Create and run crew
            logging.info("Creating crew and starting execution...")
            crew = Crew(
                agents=[researcher, coder, tester],
                tasks=[research_task, coding_task, testing_task],
                process=Process.sequential
            )
            
            logging.info("Starting crew execution...")
            result = crew.kickoff()
            logging.info("Crew execution completed")
            
            # Extract solution and test cases
            logging.debug("Extracting solution from result...")
            solution = extract_solution(result.raw)
            if solution:
                logging.debug(f"Solution extracted, length: {len(solution)}")
            else:
                logging.warning("No solution found in result")
            
            logging.debug("Extracting test cases...")
            test_cases = extract_test_cases(result.raw)
            logging.debug(f"Found {len(test_cases)} test cases")
            
            # Run tests
            logging.info("Running tests...")
            test_results = run_tests(solution, test_cases)
            
            # Save results
            results_file = self.results_manager.save_to_file(
                problem_file,
                solution,
                test_cases,
                test_results
            )
            
            return results_file
            
        except Exception as e:
            logging.error(f"Error processing problem {problem_file.name}: {str(e)}")
            return None

# --- Helper Functions ---
def extract_question(problem_definition: str) -> str:
    """Extract the main question from the problem definition."""
    question_match = re.search(r'=== Problem ===\n(.*?)(?=\n\n|$)', problem_definition, re.DOTALL)
    if question_match:
        return question_match.group(1).strip()
    return ""

def extract_examples(problem_definition: str) -> str:
    """Extract examples from the problem definition."""
    examples_match = re.search(r'Example:?\n(.*?)(?=\n\n|Constraints:|$)', problem_definition, re.DOTALL)
    if examples_match:
        return examples_match.group(1).strip()
    return ""

def extract_constraints(problem_definition: str) -> str:
    """Extract constraints from the problem definition."""
    constraints_match = re.search(r'Constraints:?\n(.*?)(?=\n\n|$)', problem_definition, re.DOTALL)
    if constraints_match:
        return constraints_match.group(1).strip()
    return ""

def extract_solution(result: str) -> str:
    """Extract the solution code from the result."""
    solution_match = re.search(r'=== Solution ===\n(.*?)(?=\n\n|=== Test Cases ===|$)', result, re.DOTALL)
    if solution_match:
        return solution_match.group(1).strip()
    return ""

def extract_test_cases(result: str) -> List[Dict[str, Any]]:
    """Extract test cases from the result."""
    test_cases = []
    test_case_pattern = r'Test Case \d+:\nInput: (.*?)\nExpected: (.*?)(?=\n\n|$)'
    
    for match in re.finditer(test_case_pattern, result, re.DOTALL):
        test_cases.append({
            'input': match.group(1).strip(),
            'expected': match.group(2).strip()
        })
    
    return test_cases

def run_tests(solution: str, test_cases: List[Dict[str, Any]]) -> str:
    """Run the test cases and return the results."""
    # Create a temporary Python file with the solution and test cases
    test_file = "temp_test.py"
    with open(test_file, "w") as f:
        f.write(solution + "\n\n")
        f.write("def run_test_cases():\n")
        for i, test_case in enumerate(test_cases, 1):
            f.write(f"    # Test Case {i}\n")
            f.write(f"    try:\n")
            f.write(f"        result = {test_case['input']}\n")
            f.write(f"        expected = {test_case['expected']}\n")
            f.write(f"        assert result == expected, f'Test Case {i} Failed: Expected {expected}, got {result}'\n")
            f.write(f"        print(f'Test Case {i} passed')\n")
            f.write(f"    except Exception as e:\n")
            f.write(f"        print(f'Test Case {i} failed: {str(e)}')\n")
    
    # Run the test file
    import subprocess
    try:
        result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)
        return result.stdout
    finally:
        # Clean up the temporary file
        if os.path.exists(test_file):
            os.remove(test_file)

# --- Main Execution ---
def main() -> None:
    """Main execution function."""
    try:
        # Setup
        setup_logging()
        load_dotenv()
        
        # Initialize problem manager and processor
        problem_manager = ProblemManager()
        processor = ProblemProcessor(solved_dir=problem_manager.solved_dir)
        
        # Get unsolved problems
        unsolved_problems = problem_manager.get_unsolved_problems()
        
        if not unsolved_problems:
            logging.info("No unsolved problems found in the unsolved directory.")
            return
        
        logging.info(f"Found {len(unsolved_problems)} unsolved problems")
        
        # Process each problem
        for problem_file in unsolved_problems:
            logging.info(f"Processing problem: {problem_file.name}")
            
            # Process the problem
            result_file = processor.process_problem(problem_file)
            
            if result_file:
                # Mark problem as solved
                problem_manager.mark_as_solved(problem_file)
                logging.info(f"Successfully processed {problem_file.name}")
            else:
                logging.error(f"Failed to process {problem_file.name}")
            
    except Exception as e:
        logging.error(f"Error during execution: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()