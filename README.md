# LeetCode Problem Status Checker

This tool automates the process of checking if specific LeetCode problems have been solved. By reading a CSV file with problem links, the script logs into LeetCode, checks each problem's solved status, and updates the CSV file accordingly.

## Features
- **Automated Problem Status Check**: The script uses Selenium to visit each problem page and detect if it’s marked as solved.
- **Manual Login**: Log into your LeetCode account manually, and the script will continue after login.
- **Progress Saving**: Updates are saved after each problem check, ensuring progress is not lost in case of interruptions.

## Prerequisites

1. **Python**: Python 3.7 or higher.
2. **Google Chrome**: Chrome browser needs to be installed.
3. **ChromeDriver**: Download the compatible version of [ChromeDriver](https://chromedriver.chromium.org/downloads) for your Chrome browser version.

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/leetcode-status-checker.git
    cd leetcode-status-checker
    ```

2. **Install Dependencies**:
    Install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download and Configure ChromeDriver**:
    - Download the ChromeDriver executable that matches your Chrome version from [here](https://chromedriver.chromium.org/downloads).
    - Update the `chrome_driver_path` in the script to the path of your ChromeDriver executable.

## Usage

1. **Prepare the Input CSV File**:
    - Create a CSV file (e.g., `Microsoft.csv`) with a column titled `problem_link` containing the URLs of LeetCode problems you want to check.

2. **Run the Script**:
    - Run the script in the terminal:
    ```bash
    python leetcode_checker.py
    ```

3. **Manual Login**:
    - When prompted, log into your LeetCode account manually in the Chrome window that opens. The script will continue automatically once login is detected.

4. **Results**:
    - The script will check each problem in the CSV and update the file with a new `SOLVED` column. The CSV file will be saved after each check to ensure progress is preserved.

## CSV Format
The input CSV file should have the following format:

| problem_link                        |
|-------------------------------------|
| https://leetcode.com/problems/abc/  |
| https://leetcode.com/problems/xyz/  |

After running the script, a `SOLVED` column will be added:

| problem_link                        | SOLVED |
|-------------------------------------|--------|
| https://leetcode.com/problems/abc/  | Yes    |
| https://leetcode.com/problems/xyz/  | No     |

## Contributing

If you would like to contribute, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License.

## Troubleshooting

- **Login Issues**: Ensure that you are able to log into LeetCode manually before running the script.
- **ChromeDriver Errors**: Ensure that the version of ChromeDriver matches your Chrome browser version. You may need to update `chrome_driver_path` if ChromeDriver is located elsewhere.
- **Timeouts**: If the script times out frequently, try increasing the wait time or checking for internet connection stability.
