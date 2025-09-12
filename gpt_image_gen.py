#!/usr/bin/env python3
"""
Simple image generator using OpenAI's DALL-E API.
Describe what you want in plain English and get an image back.
"""

import os
import sys
from openai import OpenAI
from datetime import datetime
import requests
from typing import Literal, cast
import base64


def analyze_image_with_vision(image_path, api_key=None, user_prompt=None):
    """Analyze an image using GPT-4 Vision and generate a detailed description."""

    # Get API key from environment or parameter
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OpenAI API key not found!")
        return None

    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return None

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        # Read and encode the image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        print(f"Analyzing inspiration image: {image_path}...")

        # Prepare the vision prompt
        vision_prompt = "Analyze this image in detail. Describe the style, colors, composition, mood, lighting, and any notable elements. Be specific and detailed."
        if user_prompt:
            vision_prompt += f" Also consider this user guidance: {user_prompt}"

        # Call GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o for vision capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": vision_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        description = response.choices[0].message.content
        print("✓ Image analysis complete")
        return description

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None


def generate_image(
    prompt,
    api_key=None,
    model="gpt-image-1",
    size="1024x1024",
    quality="low",
    inspiration_image=None,
):
    """Generate an image from a text prompt using OpenAI's image models."""

    # Get API key from environment or parameter
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OpenAI API key not found!")
        print("Please set OPENAI_API_KEY environment variable or pass it as argument")
        return None

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # If inspiration image is provided, analyze it first
    if inspiration_image:
        image_description = analyze_image_with_vision(
            inspiration_image, api_key, prompt
        )
        if image_description:
            # Create enhanced prompt combining image analysis and user prompt
            if prompt:
                enhanced_prompt = f"Create an image inspired by: {image_description}. Additional requirements: {prompt}"
            else:
                enhanced_prompt = (
                    f"Create an image based on this description: {image_description}"
                )

            print(f"Enhanced prompt created from image analysis")
            prompt = enhanced_prompt
        else:
            print("Warning: Could not analyze inspiration image, using original prompt")
            if not prompt:
                print("Error: No prompt provided and image analysis failed")
                return None

    try:
        print(
            f"Generating image for: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}' ..."
        )
        print(f"Model: {model}, Size: {size}, Quality: {quality}")

        # Cast parameters to proper types for OpenAI API
        size_param = cast(
            Literal[
                "1024x1024",
                "1024x1792",
                "1792x1024",
                "1024x1536",
                "1536x1024",
            ],
            size,
        )

        # Build parameters for image generation
        generate_params = {
            "model": model,
            "prompt": prompt,
            "size": size_param,
            "n": 1,
        }

        # Handle quality parameter based on model
        if model == "dall-e-3":
            # DALL-E 3 uses "standard" and "hd"
            if quality in ["low", "medium"]:
                generate_params["quality"] = "standard"
            elif quality == "high":
                generate_params["quality"] = "hd"
            else:
                generate_params["quality"] = quality  # already "standard" or "hd"
            print(f"Using DALL-E 3 with quality: {generate_params['quality']}")
        elif model == "gpt-image-1":
            # gpt-image-1 uses "low", "medium", "high"
            if quality in ["standard", "hd"]:
                # Map DALL-E 3 qualities to gpt-image-1
                generate_params["quality"] = "high" if quality == "hd" else "medium"
            else:
                generate_params["quality"] = quality
            print(f"Using gpt-image-1 with quality: {generate_params['quality']}")

        # Generate image
        print(f"Calling OpenAI API...")
        response = client.images.generate(**generate_params)

        # Get image data
        if response.data and len(response.data) > 0:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(
                c for c in prompt[:30] if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            filename = f"image_{timestamp}_{safe_prompt}.png"

            # Handle different response formats based on model
            if model == "gpt-image-1":
                # gpt-image-1 always returns base64-encoded images
                if hasattr(response.data[0], "b64_json") and response.data[0].b64_json:
                    import base64

                    print("Decoding base64 image from gpt-image-1...")
                    image_data = base64.b64decode(response.data[0].b64_json)
                    with open(filename, "wb") as f:
                        f.write(image_data)
                else:
                    print(
                        f"No b64_json in gpt-image-1 response. Available attributes: {dir(response.data[0])}"
                    )
                    return None
            else:
                # DALL-E 3 returns URLs
                if response.data[0].url:
                    image_url = response.data[0].url
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        with open(filename, "wb") as f:
                            f.write(image_response.content)
                    else:
                        print(f"Error downloading image: {image_response.status_code}")
                        return None
                else:
                    print("No URL in DALL-E response")
                    return None
        else:
            print("No image data received from API")
            return None

        print(f"✓ Image saved as: {filename}")
        return filename

    except Exception as e:
        print(f"Error generating image: {e}")
        # Show more details for debugging
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, "__dict__"):
            print(f"Error details: {e.__dict__}")
        return None


def main():
    """Main function to run the image generator."""

    import argparse

    parser = argparse.ArgumentParser(
        description="Generate images using OpenAI's gpt-image-1 model"
    )
    parser.add_argument(
        "--prompt",
        "-p",
        help="The image description prompt (if not provided, will ask interactively)",
    )
    parser.add_argument(
        "--api-key", "-k", help="OpenAI API key (overrides environment variable)"
    )
    parser.add_argument(
        "--model",
        "-m",
        default="gpt-image-1",
        choices=["dall-e-3", "gpt-image-1"],
        help="Model to use for image generation (default: gpt-image-1)",
    )
    parser.add_argument(
        "--size",
        "-s",
        default="1024x1024",
        choices=[
            "1024x1024",
            "1024x1792",
            "1792x1024",
            "1024x1536",
            "1536x1024",
        ],
        help="Image size (default: 1024x1024). DALL-E 3: 1024x1024, 1024x1792, 1792x1024. gpt-image-1: 1024x1024, 1024x1536, 1536x1024",
    )
    parser.add_argument(
        "--quality",
        "-q",
        default="low",
        choices=["low", "medium", "high", "standard", "hd"],
        help="Image quality (default: low for cost efficiency). gpt-image-1: low/medium/high. DALL-E 3: standard/hd",
    )
    parser.add_argument(
        "--inspiration-image",
        "-i",
        help="Path to an image file to use as inspiration. The image will be analyzed and used to enhance the prompt.",
    )

    args = parser.parse_args()

    # Get prompt from args or interactive mode
    if args.prompt:
        prompt = args.prompt
    else:
        # Interactive mode - only if no inspiration image or if user wants additional prompt
        if not args.inspiration_image:
            print("OpenAI Image Generator")
            print("-" * 40)
            prompt = input("Describe the image you want: ").strip()

            if not prompt:
                print("No prompt provided. Exiting.")
                return
        else:
            # With inspiration image, prompt is optional
            print("OpenAI Image Generator")
            print("-" * 40)
            print(f"Using inspiration image: {args.inspiration_image}")
            prompt = input("Additional requirements (or press Enter to skip): ").strip()

    # Generate the image with optional parameters
    result = generate_image(
        prompt,
        api_key=args.api_key,
        model=args.model,
        size=args.size,
        quality=args.quality,
        inspiration_image=args.inspiration_image,
    )

    if result:
        print("\n✓ Successfully generated image!")
    else:
        print("\n✗ Failed to generate image.")
        sys.exit(1)


if __name__ == "__main__":
    main()
