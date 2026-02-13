# Blog Writing Skill Evaluation

This directory contains the evaluation framework for the `blog-writing-guide` skill.

## Structure
- **`test_cases.json`**: A list of prompts and expected criteria for testing the skill.
- **`validate_blog_post.py`**: A Python script to validate generated posts.

## How to Run an Evaluation

1.  **Select a Test Case**: Open `test_cases.json` and pick a prompt (e.g., "Write a blog post about setting up MariaDB...").
2.  **Generate Content**: Ask Gemini (or your agent) to write the post using the skill.
    *   *Example Command*: "Using the blog-writing-guide, write a post about setting up MariaDB."
3.  **Save the File**: Save the output to `_posts/YYYY-MM-DD-your-title.md`.
4.  **Run Validation**:
    ```bash
    python3 validate_blog_post.py _posts/YYYY-MM-DD-your-title.md
    ```
5.  **Review Results**: The script will Pass or Fail based on the criteria. Update the `SKILL.md` if the agent consistently fails a specific check.
