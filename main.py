# main.py
"""
Main script for running a CrewAI crew to solve coding problems.

This script orchestrates the process of:
1. Loading problem definitions
2. Creating and configuring agents
3. Setting up and executing tasks
4. Saving and displaying results
5. Running tests on the generated solution
"""

import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, Any, Dict, List

from dotenv import load_dotenv
from crewai import Crew

from agents import Agents
from tasks import Tasks
from custom_task import CustomTask

# --- Logging Configuration ---
def setup_logging() -> None:
    """Configure logging with a clear format and appropriate level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_output_length(output: Any) -> int:
    """
    Safely get the length of an output object.
    
    Args:
        output: The output object to measure.
        
    Returns:
        The length of the output as a string, or 0 if not measurable.
    """
    if output is None:
        return 0
    return len(str(output))

def format_output(output: Any) -> str:
    """
    Format an output object into a string.
    
    Args:
        output: The output object to format.
        
    Returns:
        A string representation of the output.
    """
    if output is None:
        return "No output generated."
    return str(output)

def extract_code(solution: str) -> str:
    """
    Extract the actual code from the solution output.
    
    Args:
        solution: The solution output string.
        
    Returns:
        The extracted code, or empty string if no code found.
    """
    # Look for code blocks
    code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', solution, re.DOTALL)
    if code_blocks:
        code = code_blocks[0].strip()
        # Remove any test cases from the code
        if "if __name__ == \"__main__\":" in code:
            code = code[:code.find("if __name__ == \"__main__\":")]
        return code.strip()
    
    # If no code blocks, try to find the first function definition
    function_match = re.search(r'def\s+\w+\s*\([^)]*\):', solution)
    if function_match:
        start_idx = function_match.start()
        code = solution[start_idx:].strip()
        # Remove any test cases from the code
        if "if __name__ == \"__main__\":" in code:
            code = code[:code.find("if __name__ == \"__main__\":")]
        return code.strip()
    
    return ""

def extract_test_cases(test_cases: str) -> List[Dict[str, Any]]:
    """
    Extract test cases from the test cases output.
    
    Args:
        test_cases: The test cases output string.
        
    Returns:
        List of dictionaries containing test case information.
    """
    test_list = []
    
    # First try to find test cases in code blocks
    test_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', test_cases, re.DOTALL)
    for block in test_blocks:
        # Try to find the test_cases list definition
        test_cases_match = re.search(r'test_cases\s*=\s*\[(.*?)\]', block, re.DOTALL)
        if test_cases_match:
            test_cases_str = test_cases_match.group(1)
            # Split by comma and handle each test case
            for test_case in test_cases_str.split(','):
                test_case = test_case.strip()
                if not test_case:
                    continue
                # Remove parentheses and split into components
                test_case = test_case.strip('()')
                parts = [p.strip() for p in test_case.split(',')]
                if len(parts) >= 2:
                    input_str = f"({parts[0]}, {parts[1]})"
                    expected = parts[2].strip()
                    test_list.append({
                        'input': input_str,
                        'expected': expected
                    })
    
    # If no test cases found in blocks, try to find assert statements
    if not test_list:
        assert_statements = re.findall(r'assert\s+(\w+)\s*\((.*?)\)\s*==\s*(.*?)(?:\s*,\s*".*?")?$', test_cases, re.MULTILINE)
        for func_name, args, expected in assert_statements:
            # Handle tuple inputs
            if args.strip().startswith('(') and args.strip().endswith(')'):
                input_str = args.strip()
            else:
                input_str = f"({args.strip()})"
            
            test_list.append({
                'input': input_str,
                'expected': expected.strip()
            })
    
    return test_list

def run_tests(solution_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """
    Run the test cases on the solution code.
    
    Args:
        solution_code: The solution code to test.
        test_cases: List of test cases to run.
        
    Returns:
        A string containing the test results.
    """
    if not solution_code:
        return "No solution code found."
    if not test_cases:
        return "No test cases found."
    
    # Create a temporary module to run the code
    test_module = type(sys)(f"test_module_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    test_module.__dict__.update({
        'solution': None,  # Will be set by exec
        'test_cases': test_cases
    })
    
    try:
        # Execute the solution code
        exec(solution_code, test_module.__dict__)
        
        # Get the solution function
        solution_func = None
        for name, obj in test_module.__dict__.items():
            if callable(obj) and name != 'test_cases':
                solution_func = obj
                break
        
        if not solution_func:
            return "No solution function found in the code."
        
        # Run tests
        results = []
        for i, test in enumerate(test_cases, 1):
            try:
                # Parse input
                input_str = test['input'].strip()
                expected_str = test['expected'].strip()
                
                # Handle tuple inputs
                if input_str.startswith('(') and input_str.endswith(')'):
                    # Remove outer parentheses and split by comma
                    inner = input_str[1:-1].strip()
                    if ',' in inner:
                        # Multiple arguments
                        args = [eval(arg.strip()) for arg in inner.split(',')]
                    else:
                        # Single argument
                        args = [eval(inner)]
                else:
                    # Single argument without parentheses
                    args = [eval(input_str)]
                
                # Run solution
                actual = solution_func(*args)
                
                # Compare with expected output
                expected = eval(expected_str)
                passed = actual == expected
                
                results.append(f"Test Case {i}:")
                results.append(f"Input: {input_str}")
                results.append(f"Expected: {expected_str}")
                results.append(f"Actual: {actual}")
                results.append(f"Status: {'PASSED' if passed else 'FAILED'}")
                results.append("")
                
            except Exception as e:
                results.append(f"Test Case {i} Error: {str(e)}")
                results.append(f"Input: {test['input']}")
                results.append(f"Expected: {test['expected']}")
                results.append("")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Error running tests: {str(e)}"

# --- Problem Definition Management ---
class ProblemDefinition:
    """Handles loading and managing problem definitions."""
    
    @staticmethod
    def load_from_file(filepath: str = 'questions.txt') -> Tuple[str, str, str]:
        """
        Load problem definition from a file.
        
        Args:
            filepath: Path to the file containing the problem definition.
            
        Returns:
            Tuple containing (question, example, constraints).
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file doesn't contain the expected sections.
        """
        try:
            with open(filepath, 'r') as file:
                content = file.read()
            
            sections = content.split('\n\n')
            if len(sections) < 3:
                raise ValueError(f"Expected 3 sections, found {len(sections)}")
                
            return tuple(section.strip() for section in sections[:3])
            
        except Exception as e:
            logging.error(f"Error loading problem definition: {e}")
            raise

# --- Results Management ---
class ResultsManager:
    """Handles saving and managing results."""
    
    @staticmethod
    def save_to_file(solution: Any, test_cases: Any, test_results: str) -> Optional[str]:
        """
        Save solution, test cases, and test results to a timestamped file.
        
        Args:
            solution: The generated code solution.
            test_cases: The generated test cases.
            test_results: The results of running the tests.
            
        Returns:
            The name of the file where results were saved, or None if saving failed.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as file:
                file.write("=== Problem Solution ===\n\n")
                file.write(format_output(solution))
                file.write("\n\n=== Test Cases ===\n\n")
                file.write(format_output(test_cases))
                file.write("\n\n=== Test Results ===\n\n")
                file.write(test_results)
                
            logging.info(f"Results saved to {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            return None

# --- Task Execution ---
class TaskExecutor:
    """Handles task execution and output management."""
    
    @staticmethod
    def execute_task(task: CustomTask) -> Any:
        """
        Execute a task and store its output.
        
        Args:
            task: The task to execute.
            
        Returns:
            The output of the task execution.
            
        Raises:
            Exception: If task execution fails.
        """
        try:
            result = task.execute()
            task.set_output(result)
            return result
        except Exception as e:
            logging.error(f"Error executing task: {e}")
            raise

# --- Main Execution ---
def main() -> None:
    """Main execution function."""
    try:
        # Setup
        setup_logging()
        load_dotenv()
        
        # Load problem definition
        logging.info("Loading problem definition...")
        question, example, constraints = ProblemDefinition.load_from_file()
        
        # Create agents
        agents = Agents()
        developer = agents.developer()
        tester = agents.tester()
        
        # Create tasks
        tasks = Tasks()
        break_down_task = tasks.break_down_task(
            agent=developer,
            question=question,
            example=example,
            constraints=constraints
        )
        
        write_answer_task = tasks.write_answer_for_tasks(
            agent=developer,
            context=[break_down_task]
        )
        
        test_cases_task = tasks.test_cases(
            agent=tester,
            context=[write_answer_task]
        )
        
        # Create and run crew
        logging.info("Initializing crew...")
        crew = Crew(
            agents=[developer, tester],
            tasks=[break_down_task, write_answer_task, test_cases_task],
            verbose=True
        )
        result = crew.kickoff()
        
        # Extract task outputs
        solution = crew.tasks[1].get_output()  # write_answer_task
        test_cases = crew.tasks[2].get_output()  # test_cases_task
        
        # Extract and run tests
        logging.info("Extracting code and test cases...")
        solution_code = extract_code(format_output(solution))
        test_cases_list = extract_test_cases(format_output(test_cases))
        
        logging.info("Running tests...")
        test_results = run_tests(solution_code, test_cases_list)
        
        # Save results
        output_file = ResultsManager.save_to_file(solution, test_cases, test_results)
        
        # Display results
        print("\n--- Final Result ---")
        print(format_output(solution))
        print("\n--- Test Results ---")
        print(test_results)
        print("--------------------")
        if output_file:
            print(f"\nResults saved to: {output_file}")
            
    except Exception as e:
        logging.error(f"Error during execution: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()