import argparse
import os
from playwright.sync_api import sync_playwright, Error as PlaywrightError


def html_file_to_jpeg(
    local_html_path: str,
    output_jpeg_path: str,
    viewport_width: int = 1280,
    viewport_height: int = 720,
    quality: int = 90,
    full_page: bool = True,
    timeout_ms: int = 30000
):
    """
    Converts a local HTML file to a JPEG image using Playwright.

    Args:
        local_html_path (str): Path to the local HTML file.
        output_jpeg_path (str): Path to save the output JPEG image.
        viewport_width (int): Width of the browser viewport for initial rendering.
        viewport_height (int): Height of the browser viewport for initial rendering.
                               If full_page is False, this is the image height.
        quality (int): JPEG quality (0-100).
        full_page (bool): Whether to capture the full scrollable page.
        timeout_ms (int): Timeout in milliseconds for page navigation and screenshot.
    """
    if not os.path.exists(local_html_path):
        print(f"Error: Input HTML file not found at '{local_html_path}'")
        return
    if not os.path.isfile(local_html_path):
        print(f"Error: Input path '{local_html_path}' is not a regular file.")
        return

    if not 0 <= quality <= 100:
        raise ValueError("JPEG quality must be between 0 and 100.")

    if not output_jpeg_path.lower().endswith((".jpg", ".jpeg")):
        print(
            f"Warning: Output path '{output_jpeg_path}' does not end with .jpg or .jpeg. Appending .jpg.")
        output_jpeg_path += ".jpg"

    with sync_playwright() as p:
        browser = None
        try:
            print("Launching browser (Chromium)...")
            browser = p.chromium.launch()
        except PlaywrightError as e:
            print(f"Error: Could not launch Chromium: {e}")
            print(
                "Please ensure you have run 'playwright install chromium' or 'playwright install'.")
            return
        except Exception as e:
            print(f"An unexpected error occurred during browser launch: {e}")
            return

        page = browser.new_page()
        page.set_viewport_size(
            {"width": viewport_width, "height": viewport_height})

        try:
            # Convert local file path to an absolute path and then to a file:// URL
            abs_path = os.path.abspath(local_html_path)
            file_url = f"file://{abs_path}"
            print(f"Loading local HTML file: {file_url}")
            page.goto(file_url, wait_until="networkidle", timeout=timeout_ms)

            # Ensure output directory exists
            output_dir = os.path.dirname(output_jpeg_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Created output directory: {output_dir}")

            print(f"Taking screenshot and saving to {output_jpeg_path}...")
            screenshot_options = {
                "path": output_jpeg_path,
                "type": "jpeg",
                "quality": quality,
                "full_page": full_page,
                "timeout": timeout_ms + 10000
            }
            page.screenshot(**screenshot_options)
            print(
                f"Successfully converted '{local_html_path}' to '{output_jpeg_path}'")

        except PlaywrightError as e:  # More specific Playwright errors
            print(f"A Playwright error occurred: {e}")
            if "Timeout" in str(e):
                print(
                    f"Page navigation or screenshot timed out after {timeout_ms / 1000} seconds.")
                print(
                    "Consider increasing the timeout or checking page complexity (e.g., large local resources).")
        except Exception as e:
            print(f"An unexpected error occurred during processing: {e}")
        finally:
            if browser:
                print("Closing browser...")
                browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Convert a local HTML file to a JPEG image.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--local_html_path", help="Path to the local HTML file (e.g., 'my_document.html').")
    parser.add_argument(
        "--output_jpeg_path", help="Path to save the output JPEG image (e.g., 'output_image.jpg').")

    parser.add_argument("--width", type=int, default=1280,
                        help="Viewport width for initial page rendering.")
    parser.add_argument("--height", type=int, default=720,
                        help="Viewport height for initial page rendering. If --no-full-page, this is the image height.")
    parser.add_argument("--quality", type=int, default=90,
                        choices=range(0, 101), metavar="[0-100]", help="JPEG quality.")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Timeout in seconds for page loading and screenshot operations.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--full-page", action="store_true", dest="full_page", default=True,
                       help="Capture the full scrollable page (this is the default action).")
    group.add_argument("--no-full-page", action="store_false", dest="full_page",
                       help="Capture only the currently visible viewport area.")

    args = parser.parse_args()

    effective_height = args.height
    if args.full_page:
        if args.height == 0:
            effective_height = 720
            print(
                f"Using default initial viewport height: {effective_height}px for full page screenshot as --height was 0.")
    elif args.height == 0:
        parser.error(
            "--height cannot be 0 when --no-full-page (capturing viewport only) is specified.")

    try:
        html_file_to_jpeg(
            args.local_html_path,
            args.output_jpeg_path,
            viewport_width=args.width,
            viewport_height=effective_height,
            quality=args.quality,
            full_page=args.full_page,
            timeout_ms=args.timeout * 1000
        )
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred in the main execution: {e}")


if __name__ == "__main__":
    main()
