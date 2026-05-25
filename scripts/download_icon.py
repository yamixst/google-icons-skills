#!/usr/bin/env python3
"""
Download Material Symbols icons from Google Fonts for Android projects.
Downloads directly as Android Vector Drawable XML format.

Usage:
    python download_icon.py --search home
    python download_icon.py --name home --output ic_home.xml
    python download_icon.py --name settings --style rounded
"""

import argparse
import gzip
import json
import sys
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

METADATA_URL = "http://fonts.google.com/metadata/icons?incomplete=1&key=material_symbols"
CACHE_DIR = Path(tempfile.gettempdir()) / "google-fonts"
CACHE_FILE = CACHE_DIR / "google_icons_metadata.json"

# Material Symbols style mapping
MATERIAL_SYMBOLS_STYLES = {
    "outlined": "materialsymbolsoutlined",
    "rounded": "materialsymbolsrounded",
    "sharp": "materialsymbolssharp",
}

COMPOSE_STYLE_FAMILIES = {
    "outlined": "Material+Symbols+Outlined",
    "rounded": "Material+Symbols+Rounded",
    "sharp": "Material+Symbols+Sharp",
}

OUTPUT_FORMATS = {
    "xml": ".xml",
    "compose": ".kt",
    "apple": ".svg",
}


def fetch_metadata(force_refresh=False):
    """Fetch and cache icon metadata."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not force_refresh and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    print("Fetching icon metadata from Google Fonts...", file=sys.stderr)
    try:
        req = urllib.request.Request(
            METADATA_URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            # Remove the )]}' prefix if present
            if content.startswith(")]}'"):
                content = content[5:]
            metadata = json.loads(content)
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            return metadata
    except (urllib.error.URLError, json.JSONDecodeError, IOError) as e:
        print(f"Error fetching metadata: {e}", file=sys.stderr)
        sys.exit(1)


def search_icons(metadata, query):
    """Search icons by name."""
    results = []
    icons = metadata.get('icons', [])

    query_lower = query.lower()
    for icon in icons:
        name = icon.get('name', '')
        if query_lower in name.lower():
            results.append(icon)

    return results


def build_download_url(icon_name, style='outlined', size=24, output_format='xml'):
    """Build the download URL for the requested icon format."""
    style_folder = MATERIAL_SYMBOLS_STYLES.get(style, 'materialsymbolsoutlined')

    if output_format == 'compose':
        family = COMPOSE_STYLE_FAMILIES.get(style, 'Material+Symbols+Outlined')
        return (
            f"https://fonts.gstatic.com/render/v1/{family}/{size}dp/{icon_name}.kt"
            f"?var=opsz,wght,FILL,GRAD,ROND@{size},400,0,0,50"
        )

    extension = OUTPUT_FORMATS.get(output_format, '.xml').lstrip('.')
    return (
        f"https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/"
        f"{icon_name}/default/{size}px.{extension}"
    )


def read_text_response(response):
    """Read an HTTP response body as UTF-8 text, handling gzip when present."""
    content = response.read()
    content_encoding = response.headers.get('Content-Encoding', '').lower()

    if content_encoding == 'gzip' or content[:2] == b'\x1f\x8b':
        content = gzip.decompress(content)

    return content.decode('utf-8')


def download_material_symbols(icon_name, style='outlined', size=24, output_path=None, output_format='xml'):
    """Download a Material Symbol in the requested format."""

    url = build_download_url(
        icon_name=icon_name,
        style=style,
        size=size,
        output_format=output_format,
    )

    print(f"Downloading: {icon_name} (Material Symbols, {style}, {size}px, {output_format})", file=sys.stderr)
    print(f"URL: {url}", file=sys.stderr)

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = read_text_response(response)

            # Determine output path
            output_suffix = OUTPUT_FORMATS.get(output_format, '.xml')
            if output_path is None:
                output_file = Path(f"ic_{icon_name}{output_suffix}")
            else:
                output_file = Path(output_path)
                if output_file.suffix != output_suffix:
                    output_file = output_file.with_suffix(output_suffix)

            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Saved to: {output_file}", file=sys.stderr)
            return True

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 404:
            print(f"Icon '{icon_name}' not found for format '{output_format}' in '{style}' style.", file=sys.stderr)
            print(f"Available styles: {', '.join(MATERIAL_SYMBOLS_STYLES.keys())}", file=sys.stderr)
        return False
    except (urllib.error.URLError, IOError) as e:
        print(f"Error downloading icon: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Download Material Symbols icons from Google Fonts in XML, Compose, or SVG formats.'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-q', '--search',
        type=str,
        help='Search icons by name (partial match)'
    )
    group.add_argument(
        '-n', '--name',
        type=str,
        help='Icon name to download'
    )

    parser.add_argument(
        '-s', '--style',
        type=str,
        choices=['outlined', 'rounded', 'sharp'],
        default='outlined',
        help='Icon style (default: outlined)'
    )
    parser.add_argument(
        '-sz', '--size',
        type=int,
        choices=[18, 20, 24, 36, 48],
        default=24,
        help='Icon size in pixels (default: 24)'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['xml', 'compose', 'apple'],
        default='xml',
        help='Output format: xml, compose, or apple (SVG) (default: xml)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: ic_<name>.<ext>)'
    )
    parser.add_argument(
        '--refresh',
        action='store_true',
        help='Force refresh metadata cache'
    )

    args = parser.parse_args()

    if args.search:
        # Search mode
        metadata = fetch_metadata(force_refresh=args.refresh)
        results = search_icons(metadata, args.search)
        if not results:
            print(f"No icons found matching '{args.search}'.")
            sys.exit(0)

        print(f"Found {len(results)} icon(s) matching '{args.search}':\n")
        for icon in results[:50]:  # Limit output
            name = icon.get('name', '')
            categories = icon.get('categories', [])
            print(f"  {name}")
            if categories:
                print(f"    Categories: {', '.join(categories)}")
        if len(results) > 50:
            print(f"\n... and {len(results) - 50} more (showing first 50)")

    elif args.name:
        # Download mode
        success = download_material_symbols(
            icon_name=args.name,
            style=args.style,
            size=args.size,
            output_path=args.output,
            output_format=args.format,
        )
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
