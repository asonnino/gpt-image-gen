# Claude Development Notes

## Important Reminders

### Git Workflow
- **The main branch is protected** - Always create a new branch before making changes:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- After making changes, push the branch and create a pull request
- Never attempt to push directly to main

### Python Environment
- **Always source the virtual environment before running Python commands:**
  ```bash
  source .venv/bin/activate
  ```
- The project uses a virtual environment located in `.venv/`
- All Python dependencies are installed in this virtual environment

### Code Style Guidelines
- **Avoid using f-strings without variables:** Modern Python linting (ruff) flags `print(f"...")` when there are no variables being formatted
  - ❌ Bad: `print(f"Static text")`
  - ✅ Good: `print("Static text")`
  - ✅ Good: `print(f"Variable: {var}")`

### Project Specifics
- Main script: `gpt_image_gen.py`
- Minimum Python version: 3.8+
- Uses OpenAI API for image generation (gpt-image-1 and DALL-E 3)
- Supports image inspiration using GPT-4 Vision

### Testing
- CI runs on Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- Linting is done with ruff
- Always run `python gpt_image_gen.py --help` to verify the script works

### Common Commands
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the script
python gpt_image_gen.py --help

# Install dependencies
pip install -r requirements.txt

# Run linting
ruff check .
```