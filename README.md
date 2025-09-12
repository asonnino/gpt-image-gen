# Image Generator

A simple Python script to generate images using OpenAI's latest gpt-image-1 model by describing what you want in plain English.

## Quick Install with pipx

```bash
pipx install git+https://github.com/asonnino/openai-image-generator.git
```

Then use it from anywhere:

```bash
gpt-image-gen --prompt "a beautiful sunset"
```

## Manual Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

### Interactive mode

```bash
python generate_image.py
```

Then enter your image description when prompted.

### Command line mode

```bash
python generate_image.py --prompt "a beautiful sunset over mountains with purple clouds"

# Or use the short form
python generate_image.py -p "a beautiful sunset over mountains with purple clouds"
```

### With custom API key

```bash
python generate_image.py --prompt "a robot painting a picture" --api-key "your-api-key-here"
```

### With custom options

```bash
# Use DALL-E 3 with HD quality
python generate_image.py --prompt "a futuristic city" --model dall-e-3 --quality hd

# Generate a portrait-oriented image
python generate_image.py -p "a tall tree" --size 1024x1536

# Fast generation with low quality
python generate_image.py -p "quick sketch" --quality low

# Combine multiple options
python generate_image.py -p "sunset" -m gpt-image-1 -s 1024x1024 -q high
```

### View help

```bash
python generate_image.py --help
```

The generated image will be saved in the current directory with a timestamp and description in the filename.

## Features

- Uses OpenAI's latest gpt-image-1 model by default (2025) for superior image generation
- Low quality by default for cost efficiency (can be overridden with --quality)
- Saves images locally with descriptive filenames
- Supports both interactive and command-line usage
- Multiple resolution options per model:
  - **DALL-E 3**: 1024x1024, 1024x1792, 1792x1024
  - **gpt-image-1**: 1024x1024, 1024x1536, 1536x1024
- Better at following complex prompts and understanding nuance compared to DALL-E 3
