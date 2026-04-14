## Testing

This project includes both automated tests for the Python backend and manual validation cases for the standalone executable. The test cases for the executable can be found here ![Test Cases](test_cases.txt)

### Automated Tests (Python Source Code)

Automated tests are provided to verify the correctness of the core computational logic, including physical and optical property calculations.

#### Requirements
Install dependencies before running tests:
Ensure the test files are downloaded in the same folder as the source code
```bash
pip install -r requirements.txt
#From the project root directory run
pytest -v
