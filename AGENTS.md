# AGENT Guidelines for `mtnprojectwrapped`

These instructions apply to the entire repository.

## Coding Standards
- Use Python 3.9 or later.
- Format all Python files with **Black** (`black .`) using a line length of **120**.
- Keep indentation at 4 spaces.
- End every text file with a newline.

## Environment Setup
- Install dependencies from `requirements.txt` before running any scripts or tests:
  ```
  pip install -r requirements.txt
  ```

## Testing
- Run unit tests before each commit:
  ```
  python -m unittest discover
  ```
  If additional tests are added, ensure they can be run from the project root. Mention the test results in the PR description.

## Commit Messages
- Start each commit message with a short imperative verb ("Add …", "Fix …", "Update …").
- Provide enough context in the body to explain why the change was made.

## Pull Request Guidance
- In the PR summary, briefly mention the purpose of the change and confirm that the tests pass.
- If any tests fail or cannot be run, note this in the PR body.
