"""Parse pytest test output into per-test results."""
import re


def parse_log(log: str) -> dict[str, str]:
    """Parse test runner output into per-test results.

    Args:
        log: Full stdout+stderr output of `bash run_test.sh 2>&1`.

    Returns:
        Dict mapping test_id to status.
        - test_id: pytest native format "path::Class::method[param]"
        - status: one of "PASSED", "FAILED", "SKIPPED", "ERROR"
    """
    results = {}

    # Strip ANSI escape codes
    log = re.sub(r'\x1b\[[0-9;]*m', '', log)

    # Match pytest inline result lines:
    # "tests/unit/test_foo.py::TestClass::test_func PASSED [ 50%]"
    # Also handles parametrized tests with brackets in test id
    inline_pattern = re.compile(
        r'^((?:tests/|src/tests/)\S+::\S+.*?)\s+(PASSED|FAILED|SKIPPED|ERROR)\s+\[\s*\d+%\]',
        re.MULTILINE,
    )
    for m in inline_pattern.finditer(log):
        test_id = m.group(1).strip()
        status = m.group(2)
        results.setdefault(test_id, status)

    # Match pytest short-test-summary lines (FAILED/ERROR at top of summary):
    # "FAILED tests/unit/test_foo.py::TestClass::test_func - AssertionError"
    summary_pattern = re.compile(
        r'^(PASSED|FAILED|SKIPPED|ERROR)\s+((?:tests/|src/tests/)\S+::\S+)',
        re.MULTILINE,
    )
    for m in summary_pattern.finditer(log):
        status = m.group(1)
        test_id = m.group(2).split(' - ')[0].strip()
        results.setdefault(test_id, status)

    # Handle collection errors: "ERROR tests/foo.py" (no "::")
    collection_error_pattern = re.compile(
        r'^ERROR\s+((?:tests/|src/tests/)[^\s:]+\.py)(?!\s*::)',
        re.MULTILINE,
    )
    for m in collection_error_pattern.finditer(log):
        test_id = m.group(1).strip()
        results.setdefault(test_id, 'ERROR')

    return results

