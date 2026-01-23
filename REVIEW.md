# PR #362 Review: google-auth-library-python-oauthlib

**PR Link**: https://github.com/googleapis/google-auth-library-python-oauthlib/pull/362/
**Reviewer**: Jules (Senior Staff Software Engineer)

## 1. Conflict & Relevance Check
- **Conflicts**: None. The changes apply cleanly to the current codebase.
- **Relevance**: The PR addresses a valid use case: running the library in headless environments where standard output (print) might not be captured, but logging is. This aligns with improving observability.

## 2. Functional Correctness
- **Logic**: The implementation adds a log statement alongside the existing print statement. This correctly duplicates the output to the logger.
- **Edge Cases**:
  - The `authorization_prompt_message` is formatted before logging. This relies on the message string (which can be user-provided) accepting the `url` keyword argument. This matches existing behavior for the `print` statement, so it introduces no new risks regarding formatting.
  - The use of `_LOGGER.setLevel(logging.INFO)` effectively hardcodes the logger level to INFO for this module. This is the main functional issue (see Critical Issues).

## 3. Thoroughness
- **Scope**: The change is applied to `run_local_server` in `google_auth_oauthlib/flow.py`. This is the primary interactive entry point, so the scope is appropriate.
- **Missing Instances**: No other obvious places need similar changes for this specific feature request.

## 4. Google Python Standards
- **Logging**:
  - **Violation**: The PR sets the logger level within the library code: `_LOGGER.setLevel(logging.INFO)`.
    - **Why it's bad**: Libraries should never manually configure logging handlers or levels. This overrides the application developer's configuration. If an application developer sets the root logger to `WARNING`, this library will force its own logs to be processed at `INFO` level (though they might still be filtered by handlers), or worse, if the application relies on inheritance, this interferes with hierarchy.
  - **Correct Approach**: The library should emit logs at the appropriate level (`INFO`), and let the application developer decide whether to see them by configuring the logging system (e.g., `logging.getLogger("google_auth_oauthlib").setLevel(logging.INFO)`).

## 5. Technical Merit & Architecture
- **Approach**: Adding logging is the correct way to solve the visibility issue in headless environments.
- **Implementation**: Over-engineered by trying to force the log level. A simpler, idiomatic Python solution is to just emit the log and assume the user will configure logging if they care about it.

## 6. Testing
- **Status**: **Insufficient**. The PR does not include any tests.
- **Requirement**: A test case should be added to `tests/unit/test_flow.py` to verify that `run_local_server` emits the expected log message.

## 7. Critical Issues
- **Blocker**: `_LOGGER.setLevel(logging.INFO)` must be removed. It violates Python logging best practices and Google Python style for libraries.
- **Breaking Changes**: No breaking API changes, but the logging behavior change is intrusive.

## 8. Suggested Refactors

### Remove explicit level setting
Remove the line that sets the level.

```python
<<<<<<< SEARCH
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)
=======
_LOGGER = logging.getLogger(__name__)
>>>>>>> REPLACE
```

### Add Test Case
Add a test case to `tests/unit/test_flow.py` to verify logging.

```python
    @mock.patch("google_auth_oauthlib.flow.webbrowser", autospec=True)
    def test_run_local_server_logs_url(self, webbrowser_mock, instance, mock_fetch_token, port, caplog):
        auth_redirect_url = urllib.parse.urljoin(
            f"http://localhost:{port}", self.REDIRECT_REQUEST_PATH
        )

        # Configure caplog to capture INFO logs
        caplog.set_level(logging.INFO, logger="google_auth_oauthlib.flow")

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(partial(instance.run_local_server, port=port))

            while not future.done():
                try:
                    requests.get(auth_redirect_url)
                except requests.ConnectionError:
                    pass

            future.result()

        # Verify log message
        assert "Please visit this URL" in caplog.text
        assert instance.redirect_uri in caplog.text
```
*(Note: `caplog` is a pytest fixture. If using `unittest`, `assertLogs` would be used.)*

## Verdict
**Needs Revision**
