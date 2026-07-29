from aermodkit import Diagnostic, Severity


def test_error_blocks_execution() -> None:
    diagnostic = Diagnostic(code="AMK-TEST-001", severity=Severity.ERROR, message="invalid")
    assert diagnostic.blocks_execution is True


def test_warning_does_not_block_execution() -> None:
    diagnostic = Diagnostic(code="AMK-TEST-002", severity=Severity.WARNING, message="review")
    assert diagnostic.blocks_execution is False
