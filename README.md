# GPT Image Generator

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API-white.svg)](https://platform.openai.com/)

A simple Python script to generate images using OpenAI's latest gpt-image-1 model by describing what you want in plain English.

## Quick Install with pipx

```bash
pipx install git+https://github.com/asonnino/openai-image-generator.git
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Then use it from anywhere:

```bash
gpt-image-gen --prompt "a beautiful sunset"
```

## Usage

### Interactive mode

```bash
python gpt_image_gen.py
```

Then enter your image description when prompted.

### Command line mode

```bash
python gpt_image_gen.py --prompt "a beautiful sunset over mountains with purple clouds"

# Or use the short form
python gpt_image_gen.py -p "a beautiful sunset over mountains with purple clouds"
```

### With custom API key

```bash
python gpt_image_gen.py --prompt "a robot painting a picture" --api-key "your-api-key-here"
```

### With custom options

```bash
# Use DALL-E 3 with HD quality
python gpt_image_gen.py --prompt "a futuristic city" --model dall-e-3 --quality hd

# Generate a portrait-oriented image
python gpt_image_gen.py -p "a tall tree" --size 1024x1536

# Fast generation with low quality
python gpt_image_gen.py -p "quick sketch" --quality low

# Combine multiple options
python gpt_image_gen.py -p "sunset" -m gpt-image-1 -s 1024x1024 -q high
```

### Using an image as inspiration

```bash
# Use an image as sole inspiration (analyzes the image and generates based on it)
python gpt_image_gen.py --inspiration-image sunset.jpg

# Combine image inspiration with custom prompt
python gpt_image_gen.py --inspiration-image sunset.jpg --prompt "make it more vibrant with purple clouds"

# Short form
python gpt_image_gen.py -i reference.png -p "transform into cyberpunk style"
```

### View help

```bash
python gpt_image_gen.py --help
```

The generated image will be saved in the current directory with a timestamp and description in the filename.

## Features

- Uses OpenAI's latest gpt-image-1 model by default (2025) for superior image generation
- **Image inspiration**: Use any image as inspiration - analyzes it with GPT-4 Vision to enhance your prompts
- Low quality by default for cost efficiency (can be overridden with --quality)
- Saves images locally with descriptive filenames
- Supports both interactive and command-line usage
- Multiple resolution options per model:
  - **DALL-E 3**: 1024x1024, 1024x1792, 1792x1024
  - **gpt-image-1**: 1024x1024, 1024x1536, 1536x1024
- Better at following complex prompts and understanding nuance compared to DALL-E 3
