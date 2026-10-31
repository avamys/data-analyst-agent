"""Specialist Agents - Domain experts for different analysis types"""

from langchain_experimental.tools import PythonREPLTool
import logging
import time
import re
from typing import Tuple
from agent.core.base_agent import BaseAgent
from agent.core.template_manager import prompt_templates
from agent.states import SubTask, TaskResult, HierarchicalState


logger = logging.getLogger(__name__)


class CodeExecutor:
    """
    Handles Python code execution and error detection

    Responsibilities:
    - Execute Python code using PythonREPLTool
    - Detect execution errors from output
    - Extract error messages
    - Clean up code formatting
    """

    def __init__(self):
        self.python_tool = PythonREPLTool()
        self.logger = logging.getLogger(__name__ + ".CodeExecutor")

    def execute(self, code: str, task_id: str) -> Tuple[bool, str, str, float]:
        """
        Execute Python code and return (success, output, error, execution_time)

        Args:
            code: Python code to execute
            task_id: Task identifier for logging

        Returns:
            Tuple of (success: bool, output: str, error: str, execution_time: float)
        """
        # Clean up code formatting
        code = self._clean_code(code)

        self.logger.info(f"Executing code for {task_id}:\n{code[:300]}...")

        try:
            start_time = time.time()
            output = self.python_tool.run(code)
            execution_time = time.time() - start_time

            # Check if output contains error indicators
            # PythonREPLTool returns errors as strings, not exceptions
            if self._has_execution_error(output):
                error_msg = self._extract_error_message(output)
                self.logger.error(f"✗ Code execution failed: {error_msg}")
                return False, output, error_msg, execution_time

            self.logger.info(f"✓ Code executed successfully in {execution_time:.2f}s")
            return True, output, None, execution_time
        except Exception as e:
            # This catches issues with the tool itself, not the executed code
            error_msg = str(e)
            self.logger.error(f"✗ Tool execution failed: {error_msg}")
            return False, f"TOOL ERROR: {error_msg}", error_msg, 0.0

    def _clean_code(self, code: str) -> str:
        """Remove markdown code fences from generated code"""
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()
        return code

    def _has_execution_error(self, output: str) -> bool:
        """
        Check if the output contains Python error indicators

        Common patterns:
        - Traceback (most recent call last):
        - Error: <ErrorType>
        - Exception: <message>
        - <ErrorType>Error: <message>
        - FileNotFoundError(...) - compact error format
        """
        if not output:
            return False

        error_patterns = [
            r"Traceback \(most recent call last\):",
            r"\w+Error:",  # NameError: message format
            r"\w+Exception:",  # SomeException: message format
            r"^\s*File \".*\", line \d+",  # Stack trace lines
            r"^\w+Error\(",  # FileNotFoundError(...) compact format
            r"^\w+Exception\(",  # SomeException(...) compact format
        ]

        for pattern in error_patterns:
            if re.search(pattern, output, re.MULTILINE):
                return True

        return False

    def _extract_error_message(self, output: str) -> str:
        """
        Extract the actual error message from the output

        Handles both full tracebacks and compact error formats
        """
        lines = output.strip().split("\n")

        # Look for the last line that looks like an error
        # Try both "Error:" format and "Error(...)" format
        for line in reversed(lines):
            if re.search(r"\w+(Error|Exception)(:|\()", line):
                return line.strip()

        # If no specific error line found, return last few lines
        return "\n".join(lines[-3:]) if len(lines) >= 3 else output


class InsightExtractor:
    """
    Extracts key insights from code execution output

    Responsibilities:
    - Parse output text for insights using regex patterns
    - Filter and rank insights by quality
    - Return structured insight list
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".InsightExtractor")

    def extract(self, output: str) -> list:
        """
        Extract key insights from code output

        Args:
            output: String output from code execution

        Returns:
            List of insight strings (max 5)
        """
        insights = []

        # Look for lines with key findings patterns
        patterns = [
            r"(Key finding|Insight|Conclusion|Result|Finding):\s*(.+)",
            r"(shows?|indicates?|suggests?|reveals?)\s+(.+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            for match in matches:
                insight = match[1] if len(match) > 1 else match[0]
                if len(insight) > 10:  # Filter out too short
                    insights.append(insight.strip())

        # Also extract any lines starting with "- " (bullet points)
        bullet_insights = re.findall(r"^-\s+(.+)$", output, re.MULTILINE)
        insights.extend([b.strip() for b in bullet_insights if len(b) > 15])

        return insights[:5]  # Top 5 insights


class CodeGenerator:
    """
    Generates Python code using LLM

    Responsibilities:
    - Build prompts for different specialist types
    - Get previous findings from dependencies
    - Build error feedback prompts for retries
    - Invoke LLM to generate code
    """

    def __init__(self, specialist_type: str, llm):
        self.specialist_type = specialist_type
        self.llm = llm
        self.logger = logging.getLogger(__name__ + ".CodeGenerator")

    def generate(self, task: SubTask, state: HierarchicalState) -> str:
        """
        Generate code for a task

        Args:
            task: Task to generate code for
            state: Current state with context

        Returns:
            Generated Python code as string
        """
        prompt = self._build_prompt(task, state)
        response = self.llm.invoke(prompt)
        code = (
            response.content.strip() if hasattr(response, "content") else str(response)
        )
        return code

    def generate_with_error_feedback(
        self,
        task: SubTask,
        state: HierarchicalState,
        failed_code: str,
        error_message: str,
        attempt: int,
        max_retries: int,
    ) -> str:
        """
        Generate corrected code based on error feedback

        Args:
            task: Original task
            state: Current state
            failed_code: Code that failed to execute
            error_message: Error message from execution
            attempt: Current attempt number
            max_retries: Maximum retry attempts

        Returns:
            Corrected Python code as string
        """
        original_prompt = self._build_prompt(task, state)
        feedback_prompt = self._build_error_feedback_prompt(
            original_prompt=original_prompt,
            failed_code=failed_code,
            error_message=error_message,
            attempt=attempt,
            max_retries=max_retries,
        )
        response = self.llm.invoke(feedback_prompt)
        code = (
            response.content.strip() if hasattr(response, "content") else str(response)
        )
        return code

    def _build_prompt(self, task: SubTask, state: HierarchicalState) -> str:
        """Build prompt based on specialist type"""
        previous_findings = self._get_previous_findings(task, state)

        if self.specialist_type == "eda":
            return prompt_templates.render(
                "specialists/eda_analysis.jinja2",
                task_description=task.description,
                dataset_path=state.dataset_path,
                n_rows=state.dataset_profile.n_rows,
                n_cols=state.dataset_profile.n_cols,
                columns=", ".join(state.dataset_profile.feature_types.keys()),
                target_column=state.dataset_profile.target_column or "None",
                previous_findings=previous_findings,
            )
        elif self.specialist_type == "statistical":
            return prompt_templates.render(
                "specialists/statistical_analysis.jinja2",
                task_description=task.description,
                dataset_path=state.dataset_path,
                n_rows=state.dataset_profile.n_rows,
                numeric_features=", ".join(state.dataset_profile.numeric_features),
                categorical_features=", ".join(
                    state.dataset_profile.categorical_features
                ),
                target_column=state.dataset_profile.target_column,
                target_type=state.dataset_profile.target_type,
                previous_findings=previous_findings,
            )
        elif self.specialist_type == "ml":
            return prompt_templates.render(
                "specialists/ml_analysis.jinja2",
                task_description=task.description,
                dataset_path=state.dataset_path,
                n_rows=state.dataset_profile.n_rows,
                target_column=state.dataset_profile.target_column,
                target_type=state.dataset_profile.target_type,
                n_numeric=len(state.dataset_profile.numeric_features),
                n_categorical=len(state.dataset_profile.categorical_features),
                has_imbalance=state.dataset_profile.has_imbalance,
                previous_findings=previous_findings,
            )
        else:
            raise ValueError(f"Unknown specialist type: {self.specialist_type}")

    def _get_previous_findings(self, task: SubTask, state: HierarchicalState) -> str:
        """Get findings from dependent tasks"""
        if not task.dependencies:
            return "No previous findings (this is a starting task)."

        findings = []
        for dep_id in task.dependencies:
            dep_result = next(
                (r for r in state.completed_tasks if r.task_id == dep_id), None
            )
            if dep_result and dep_result.success:
                findings.append(f"\n[From {dep_id}]:\n{dep_result.output[:500]}...")

        return (
            "\n".join(findings)
            if findings
            else "Dependencies completed but no detailed output available."
        )

    def _build_error_feedback_prompt(
        self,
        original_prompt: str,
        failed_code: str,
        error_message: str,
        attempt: int,
        max_retries: int,
    ) -> str:
        """
        Build a feedback prompt when code execution fails

        Args:
            original_prompt: The original task prompt
            failed_code: The code that failed to execute
            error_message: The error message from execution
            attempt: Current attempt number
            max_retries: Maximum retry attempts

        Returns:
            Enhanced prompt with error feedback
        """
        feedback_prompt = f"""
{original_prompt}

EXECUTION ERROR - ATTEMPT {attempt}/{max_retries + 1}

Your previous code attempt failed with the following error:

```python
{failed_code}
```

ERROR MESSAGE:
{error_message}

Please analyze the error and provide a corrected version of the code that:
1. Fixes the specific error mentioned above
2. Handles potential edge cases that might cause similar errors
3. Still accomplishes the original task requirements

IMPORTANT: Respond with ONLY the corrected Python code, nothing else.
"""
        return feedback_prompt


class CodeExecutionAgent(BaseAgent):
    """
    Unified code execution agent for all specialist types

    Orchestrates three specialized components:
    - CodeGenerator: Handles LLM interaction and prompt building
    - CodeExecutor: Executes Python code and detects errors
    - InsightExtractor: Extracts insights from output

    Responsibilities:
    - Coordinate the workflow (generate → execute → extract)
    - Handle retry logic when execution fails
    - Compose results into TaskResult
    """

    def __init__(self, specialist_type: str, max_retries: int = 2, **kwargs):
        """
        Initialize code execution agent

        Args:
            specialist_type: One of "eda", "statistical", "ml"
            max_retries: Maximum number of retry attempts if code execution fails (default: 2)
            **kwargs: Additional config passed to BaseAgent
        """
        super().__init__(agent_type=specialist_type, **kwargs)
        self.specialist_type = specialist_type
        self.max_retries = max_retries

        # Compose specialized components
        self.code_generator = CodeGenerator(specialist_type, self.llm)
        self.code_executor = CodeExecutor()
        self.insight_extractor = InsightExtractor()

    def execute(self, task: SubTask, state: HierarchicalState) -> TaskResult:
        """
        Execute code generation and execution task with retry mechanism

        Workflow:
        1. Generate code using CodeGenerator
        2. Execute code using CodeExecutor
        3. Extract insights using InsightExtractor
        4. Retry with error feedback if execution fails

        Args:
            task: Task to execute
            state: Current hierarchical state

        Returns:
            TaskResult with code, output, and insights
        """
        # Retry loop with feedback
        attempt = 0
        last_code = None
        last_error = None
        total_exec_time = 0.0

        while attempt <= self.max_retries:
            attempt += 1

            # Generate code (with error feedback if retry)
            if last_error:
                self.logger.info(
                    f"Retry attempt {attempt}/{self.max_retries + 1} for {task.id}"
                )
                code = self.code_generator.generate_with_error_feedback(
                    task=task,
                    state=state,
                    failed_code=last_code,
                    error_message=last_error,
                    attempt=attempt,
                    max_retries=self.max_retries,
                )
            else:
                code = self.code_generator.generate(task, state)

            # Execute code
            success, output, error, exec_time = self.code_executor.execute(
                code, task.id
            )
            total_exec_time += exec_time

            # If successful, extract insights and return
            if success:
                insights = self.insight_extractor.extract(output)
                retry_info = f" (succeeded on attempt {attempt})" if attempt > 1 else ""
                self.logger.info(f"✓ Task {task.id} completed successfully{retry_info}")

                return TaskResult(
                    task_id=task.id,
                    specialist=self.specialist_type,
                    description=task.description,
                    code=code,
                    output=output,
                    execution_time=total_exec_time,
                    success=True,
                    error=None,
                    insights=insights,
                    metadata={
                        "strategy": task.strategy.value,
                        "attempts": attempt,
                        "retries": attempt - 1,
                    },
                )

            # If failed, prepare for retry
            last_code = code
            last_error = error

            if attempt > self.max_retries:
                self.logger.error(f"✗ Task {task.id} failed after {attempt} attempts")
                break

        # All retries exhausted, return failure
        return TaskResult(
            task_id=task.id,
            specialist=self.specialist_type,
            description=task.description,
            code=last_code,
            output=output,
            execution_time=total_exec_time,
            success=False,
            error=last_error,
            insights=[],
            metadata={
                "strategy": task.strategy.value,
                "attempts": attempt,
                "retries": attempt - 1,
                "exhausted_retries": True,
            },
        )


# Factory function - simple and clean
def get_specialist(specialist_type: str, max_retries: int = 2) -> CodeExecutionAgent:
    """
    Get specialist instance by type

    Args:
        specialist_type: One of "eda", "statistical", "ml"
        max_retries: Maximum number of retry attempts if code execution fails (default: 2)

    Returns:
        CodeExecutionAgent configured for that specialist type

    Example:
        >>> eda_specialist = get_specialist("eda")
        >>> stat_specialist = get_specialist("statistical", max_retries=3)
    """
    if specialist_type not in ["eda", "statistical", "ml"]:
        raise ValueError(
            f"Unknown specialist type: {specialist_type}. "
            f"Must be one of: eda, statistical, ml"
        )

    return CodeExecutionAgent(specialist_type=specialist_type, max_retries=max_retries)
