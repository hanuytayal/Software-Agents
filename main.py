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
            
            # Create tasks with detailed logging
            logging.debug("Creating tasks...")
            research_task = Task(
                description=f"Research and analyze this problem:\n\n{problem_definition}\n\nFocus on:\n1. Problem requirements and constraints\n2. Edge cases to consider\n3. Common pitfalls to avoid",
                agent=researcher,
                expected_output="Expected research output here"
            )
            
            coding_task = Task(
                description="""Write Python code to solve the problem. Include:
1. Clear function/class definition
2. Comprehensive docstring with examples
3. Efficient implementation
4. Error handling where appropriate
5. Comments explaining complex logic""",
                agent=coder,
                expected_output="""A complete Python implementation that:
1. Correctly solves the given problem
2. Includes proper documentation and comments
3. Handles edge cases and errors appropriately
4. Follows Python best practices and coding standards"""
            )
            
            testing_task = Task(
                description="""Create comprehensive test cases for the solution. Include:
1. Basic test cases from the problem description
2. Edge cases and boundary conditions
3. Error cases and invalid inputs
4. Performance test cases for large inputs
5. Format each test case as:
   ```python
   test_cases = [
       (input1, input2, ..., expected_output1),
       (input3, input4, ..., expected_output2),
       ...
   ]
   ```
   Or as print statements with comments:
   ```python
   # Input: [2, 7, 11, 15], target = 9
   # Expected Output: [0, 1]
   print(twoSum([2, 7, 11, 15], 9))
   ```""",
                agent=tester,
                expected_output="""A comprehensive set of test cases that:
1. Validates the solution against the problem requirements
2. Covers all edge cases and boundary conditions
3. Tests error handling and invalid inputs
4. Includes performance tests for large inputs
5. Is formatted in a clear, executable Python format"""
            )
            logging.debug("All tasks created")
            
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
            logging.debug(f"Raw result length: {len(result.raw)}")
            
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
            logging.debug(f"Test results length: {len(test_results)}")
            
            # Save results
            logging.info("Saving results...")
            result_file = self.results_manager.save_to_file(problem_file, solution, test_cases, test_results)
            logging.info(f"Results saved to: {result_file}")
            
            return result_file
            
        except Exception as e:
            logging.error(f"Error processing {problem_file.name}: {str(e)}", exc_info=True)
            return None

# --- Helper Functions ---
def extract_solution(result: str) -> str:
    """Extract solution code from the result string."""
    try:
        logging.debug("Attempting to extract solution code...")
        solution_match = re.search(r'```(?:python)?\n(.*?)\n```', result, re.DOTALL)
        if solution_match:
            solution = solution_match.group(1).strip()
            logging.debug(f"Solution extracted, length: {len(solution)}")
            return solution
        logging.warning("No solution code block found in result")
        return ""
    except Exception as e:
        logging.error(f"Error extracting solution: {str(e)}", exc_info=True)
        return ""

def extract_test_cases(test_cases: str) -> List[Dict[str, Any]]:
    """Extract test cases from the test cases output."""
    test_list = []
    logging.debug("Starting test case extraction...")
    
    try:
        # Try to find test cases in code blocks first
        test_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', test_cases, re.DOTALL)
        logging.debug(f"Found {len(test_blocks)} code blocks")
        
        for block in test_blocks:
            # Look for test case definitions
            test_cases_match = re.search(r'test_cases\s*=\s*\[(.*?)\]', block, re.DOTALL)
            if test_cases_match:
                test_cases_str = test_cases_match.group(1)
                logging.debug(f"Found test_cases list: {test_cases_str[:100]}...")
                
                for test_case in test_cases_str.split(','):
                    try:
                        test_case = test_case.strip()
                        if not test_case:
                            continue
                        test_case = test_case.strip('()')
                        parts = [p.strip() for p in test_case.split(',')]
                        if len(parts) >= 2:
                            input_str = f"({', '.join(parts[:-1])})"
                            expected = parts[-1].strip()
                            test_list.append({
                                'input': input_str,
                                'expected': expected
                            })
                            logging.debug(f"Added test case - Input: {input_str}, Expected: {expected}")
                    except Exception as e:
                        logging.error(f"Error parsing test case '{test_case}': {str(e)}")
        
        # If no test cases found in code blocks, try to find print statements
        if not test_list:
            logging.debug("No test cases found in code blocks, trying print statements...")
            print_statements = re.findall(r'print\((.*?)\)', test_cases)
            for stmt in print_statements:
                try:
                    comment_match = re.search(r'#\s*Input:\s*(.*?)\n.*?#\s*Expected Output:\s*(.*?)(?:\n|$)', stmt, re.DOTALL)
                    if comment_match:
                        input_str = comment_match.group(1).strip()
                        expected = comment_match.group(2).strip()
                        test_list.append({
                            'input': input_str,
                            'expected': expected
                        })
                        logging.debug(f"Added test case from print - Input: {input_str}, Expected: {expected}")
                except Exception as e:
                    logging.error(f"Error parsing print statement '{stmt}': {str(e)}")
        
        # If still no test cases found, try to find assert statements
        if not test_list:
            logging.debug("No test cases found in print statements, trying assert statements...")
            assert_statements = re.findall(r'assert\s+(\w+)\s*\((.*?)\)\s*==\s*(.*?)(?:\s*,\s*".*?")?$', test_cases, re.MULTILINE)
            for func_name, args, expected in assert_statements:
                try:
                    input_str = args.strip() if args.strip().startswith('(') and args.strip().endswith(')') else f"({args.strip()})"
                    test_list.append({
                        'input': input_str,
                        'expected': expected.strip()
                    })
                    logging.debug(f"Added test case from assert - Input: {input_str}, Expected: {expected.strip()}")
                except Exception as e:
                    logging.error(f"Error parsing assert statement - func: {func_name}, args: {args}: {str(e)}")
        
        logging.info(f"Total test cases extracted: {len(test_list)}")
        return test_list
        
    except Exception as e:
        logging.error(f"Error extracting test cases: {str(e)}", exc_info=True)
        return []

def run_tests(solution_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """Run the test cases on the solution code."""
    logging.info("Starting test execution...")
    
    if not solution_code or not test_cases:
        logging.warning("No solution code or test cases provided")
        return "No solution code or test cases found."
    
    try:
        # Create a temporary module to run the code
        module_name = f"test_module_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logging.debug(f"Creating temporary module: {module_name}")
        test_module = type(sys)(module_name)
        test_module.__dict__.update({
            'solution': None,
            'test_cases': test_cases
        })
        
        # Execute the solution code
        logging.debug("Executing solution code...")
        exec(solution_code, test_module.__dict__)
        
        # Get the solution function or class
        solution_func = None
        solution_class = None
        for name, obj in test_module.__dict__.items():
            if name == 'Solution':
                solution_class = obj
                logging.debug("Found Solution class")
                break
            elif callable(obj) and name != 'test_cases':
                solution_func = obj
                logging.debug(f"Found solution function: {name}")
                break
        
        if not (solution_func or solution_class):
            logging.error("No solution function or class found")
            return "No solution function or class found in the code."
        
        # Create instance if it's a class
        if solution_class:
            logging.debug("Creating Solution class instance...")
            solution_instance = solution_class()
            # Try to find the main method
            for method_name in ['isMatch', 'twoSum', 'reverseList', 'search', 'sortArray']:
                if hasattr(solution_instance, method_name):
                    solution_func = getattr(solution_instance, method_name)
                    logging.debug(f"Found method: {method_name}")
                    break
            if not solution_func:
                logging.error("No suitable method found in Solution class")
                return "No suitable method found in Solution class."
        else:
            logging.info(f"Using standalone function: {solution_func.__name__}")
        
        # Run tests
        results = []
        passed_count = 0
        total_count = len(test_cases)
        
        logging.info(f"Running {total_count} test cases...")
        for i, test in enumerate(test_cases, 1):
            try:
                input_str = test['input'].strip()
                expected_str = test['expected'].strip()
                logging.debug(f"Running test case {i}/{total_count} - Input: {input_str}")
                
                # Handle tuple inputs
                if input_str.startswith('(') and input_str.endswith(')'):
                    inner = input_str[1:-1].strip()
                    args = [eval(arg.strip()) for arg in inner.split(',')] if ',' in inner else [eval(inner)]
                else:
                    args = [eval(input_str)]
                
                # Run solution
                actual = solution_func(*args)
                expected = eval(expected_str)
                passed = actual == expected
                
                if passed:
                    passed_count += 1
                    logging.debug(f"Test case {i} passed")
                else:
                    logging.warning(f"Test case {i} failed - Expected: {expected}, Got: {actual}")
                
                results.append(f"Test Case {i}:")
                results.append(f"Input: {input_str}")
                results.append(f"Expected: {expected_str}")
                results.append(f"Actual: {actual}")
                results.append(f"Status: {'PASSED' if passed else 'FAILED'}")
                results.append("")
                
            except Exception as e:
                logging.error(f"Error running test case {i}: {str(e)}", exc_info=True)
                results.append(f"Test Case {i} Error: {str(e)}")
                results.append(f"Input: {test['input']}")
                results.append(f"Expected: {test['expected']}")
                results.append("")
        
        # Add summary
        summary = f"\nTest Summary: {passed_count}/{total_count} tests passed"
        logging.info(summary)
        results.append(summary)
        
        return "\n".join(results)
        
    except Exception as e:
        error_msg = f"Error running tests: {str(e)}"
        logging.error(error_msg, exc_info=True)
        return error_msg

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