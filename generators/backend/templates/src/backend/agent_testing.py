"""
Testing utilities for agents and workflows
"""
import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from agent_builder import AgentConfig, WorkflowConfig

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """A test case for an agent or workflow"""
    name: str
    description: str
    input_messages: List[Dict[str, str]]
    expected_outputs: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.expected_outputs is None:
            self.expected_outputs = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TestResult:
    """Result of running a test case"""
    test_name: str
    passed: bool
    actual_output: str
    expected_output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


class AgentTester:
    """Test framework for agents"""

    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []

    def add_test_case(
        self,
        name: str,
        description: str,
        input_messages: List[Dict[str, str]],
        expected_outputs: List[str] = None
    ) -> TestCase:
        """Add a test case"""
        test_case = TestCase(
            name=name,
            description=description,
            input_messages=input_messages,
            expected_outputs=expected_outputs or []
        )
        self.test_cases.append(test_case)
        return test_case

    async def run_test_case(
        self,
        test_case: TestCase,
        orchestrator,
        user_id: str = "test_user"
    ) -> TestResult:
        """Run a single test case"""
        logger.info(f"Running test case: {test_case.name}")

        start_time = datetime.utcnow()

        try:
            # Collect all outputs from the orchestrator
            outputs = []
            async for output in orchestrator.process_conversation(user_id, test_case.input_messages):
                outputs.append(output)

            actual_output = "\n".join(outputs)

            # Simple pass/fail - passes if we got output without errors
            passed = bool(actual_output) and not actual_output.startswith("Error:")

            # If expected outputs provided, check if any match
            if test_case.expected_outputs:
                passed = any(expected in actual_output for expected in test_case.expected_outputs)

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            result = TestResult(
                test_name=test_case.name,
                passed=passed,
                actual_output=actual_output,
                expected_output=test_case.expected_outputs[0] if test_case.expected_outputs else None,
                execution_time=execution_time
            )

        except Exception as e:
            logger.error(f"Test case {test_case.name} failed with error: {e}")
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            result = TestResult(
                test_name=test_case.name,
                passed=False,
                actual_output="",
                error=str(e),
                execution_time=execution_time
            )

        self.results.append(result)
        return result

    async def run_all_tests(
        self,
        orchestrator,
        user_id: str = "test_user"
    ) -> List[TestResult]:
        """Run all test cases"""
        logger.info(f"Running {len(self.test_cases)} test cases")

        self.results = []
        for test_case in self.test_cases:
            result = await self.run_test_case(test_case, orchestrator, user_id)
            logger.info(f"Test {test_case.name}: {'PASSED' if result.passed else 'FAILED'}")

        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0,
            "results": [r.to_dict() for r in self.results]
        }

    def export_results(self, filepath: str):
        """Export test results to JSON file"""
        summary = self.get_summary()
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Test results exported to {filepath}")


class WorkflowValidator:
    """Validator for workflow configurations"""

    @staticmethod
    def validate_workflow(workflow: WorkflowConfig, available_agents: List[str]) -> List[str]:
        """Validate a workflow configuration and return list of errors"""
        errors = []

        # Check if workflow has agents
        if not workflow.agents:
            errors.append("Workflow must have at least one agent")

        # Check if all agents exist
        for agent_name in workflow.agents:
            if agent_name not in available_agents:
                errors.append(f"Agent '{agent_name}' not found in registry")

        # Validate max iterations
        if workflow.max_iterations < 1:
            errors.append("max_iterations must be at least 1")

        # Pattern-specific validations
        if workflow.pattern == "hierarchical":
            if len(workflow.agents) < 2:
                errors.append("Hierarchical pattern requires at least 2 agents (1 coordinator + workers)")

        return errors

    @staticmethod
    def validate_agent(agent: AgentConfig) -> List[str]:
        """Validate an agent configuration and return list of errors"""
        errors = []

        # Check required fields
        if not agent.name:
            errors.append("Agent must have a name")

        if not agent.description:
            errors.append("Agent must have a description")

        if not agent.instructions:
            errors.append("Agent must have instructions")

        # Validate temperature
        if not (0 <= agent.temperature <= 1):
            errors.append("Temperature must be between 0 and 1")

        # Validate max_tokens if set
        if agent.max_tokens is not None and agent.max_tokens < 1:
            errors.append("max_tokens must be positive")

        return errors


# Predefined test cases for common scenarios
SAMPLE_TEST_CASES = [
    TestCase(
        name="simple_blog_request",
        description="Test simple blog post generation",
        input_messages=[
            {"role": "user", "content": "Write a blog post about Python programming"}
        ],
        expected_outputs=["blog", "python", "programming"]
    ),
    TestCase(
        name="complex_analysis",
        description="Test complex analysis request",
        input_messages=[
            {"role": "user", "content": "Analyze the pros and cons of microservices architecture"}
        ],
        expected_outputs=["pros", "cons", "microservices"]
    ),
    TestCase(
        name="creative_writing",
        description="Test creative writing capabilities",
        input_messages=[
            {"role": "user", "content": "Write a creative story about space exploration"}
        ],
        expected_outputs=["space", "story"]
    )
]


def load_sample_tests(tester: AgentTester):
    """Load sample test cases into a tester"""
    for test_case in SAMPLE_TEST_CASES:
        tester.test_cases.append(test_case)
    logger.info(f"Loaded {len(SAMPLE_TEST_CASES)} sample test cases")
