---
name: google-icons
description: Download Material Symbols icons from Google Fonts as Android Vector Drawable XML, SVG, or Android Compose Kotlin. Search icons by name, multiple styles supported (outlined, rounded, sharp).
---

# Google Icons Skill

This skill provides tools to search and download Material Symbols icons from Google Fonts for Android, web, and Apple development. Icons can be downloaded as Android Vector Drawable XML, SVG, or Android Compose Kotlin.

## Overview

Material Symbols are Google's modern icon set, available in three styles:
- **Outlined** (default): Thin strokes, minimalist design
- **Rounded**: Soft, rounded corners
- **Sharp**: Angular, precise edges

Supported download formats:
- **Android XML**: Android Vector Drawable XML, ready to use in `res/drawable`
- **SVG**: Standard SVG asset, including custom Fill, Weight, and Grade variants
- **Android Compose**: Kotlin `ImageVector` source file
- **Apple**: Compatibility alias for the default SVG asset

Supported variable font axes:
- **Fill**: `0` for outlined, `1` for filled
- **Weight**: `100` to `700`
- **Grade**: `-25` to `200`

The script works on **Linux, macOS, and Windows**.

## Quick Start

### Search for Icons
```bash
python scripts/download_icon.py --search home
```

### Download an Icon
```bash
python scripts/download_icon.py --name home --output app/src/main/res/drawable/ic_home.xml
```

### Download a Compose Icon
```bash
python scripts/download_icon.py --name toggle_on --style sharp --format compose --fill 1 --weight 700 --grade 200 --output ToggleOn.kt
```

### Download an Apple SVG
```bash
python scripts/download_icon.py --name toggle_on --style sharp --format apple --output toggle_on.svg
```

### Download a Variant SVG
```bash
python scripts/download_icon.py --name toggle_on --style sharp --format svg --fill 1 --weight 700 --grade 200 --output toggle_on.svg
```

## Script Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--search` | `-q` | Search icons by name (lists matching icons) | - |
| `--name` | `-n` | Icon name to download | - |
| `--style` | `-s` | Icon style: `outlined`, `rounded`, `sharp` | `outlined` |
| `--size` | `-sz` | Size in px: `18`, `20`, `24`, `36`, `48` | `24` |
| `--format` | `-f` | Output format: `xml`, `svg`, `compose`, `apple` | `xml` |
| `--fill` | - | Fill axis: `0` or `1` | `0` |
| `--weight` | - | Weight axis: `100` to `700` | `400` |
| `--grade` | - | Grade axis: `-25` to `200` | `0` |
| `--output` | `-o` | Output file path (default: `ic_<name>.<ext>`) | `./ic_<name>.<ext>` |
| `--refresh` | - | Force refresh metadata cache | `False` |

## Usage Examples

### Search Icons
```bash
# Find icons containing "home"
python scripts/download_icon.py --search home

# Find icons containing "settings"
python scripts/download_icon.py --search settings
```

### Download Icons

```bash
# Basic download (outlined, 24px) - produces XML
python scripts/download_icon.py --name home --output app/src/main/res/drawable/ic_home.xml

# Rounded style
python scripts/download_icon.py --name settings --style rounded --output app/src/main/res/drawable/ic_settings.xml

# Sharp style with custom size
python scripts/download_icon.py --name delete --style sharp --size 48 --output app/src/main/res/drawable/ic_delete_48.xml

# Filled heavy XML variant
python scripts/download_icon.py --name toggle_on --style sharp --fill 1 --weight 700 --grade 200 --output app/src/main/res/drawable/ic_toggle_on_filled.xml

# Filled heavy SVG variant
python scripts/download_icon.py --name toggle_on --style sharp --format svg --fill 1 --weight 700 --grade 200 --output assets/toggle_on.svg

# Android Compose Kotlin source
python scripts/download_icon.py --name toggle_on --style sharp --format compose --fill 1 --weight 700 --grade 200 --output app/src/main/java/icons/ToggleOn.kt

# Apple SVG alias (default axes only)
python scripts/download_icon.py --name toggle_on --style sharp --format apple --output Assets/toggle_on.svg
```

## Using Downloaded Icons in Android

Icons downloaded with `--format xml` are ready to use immediately as Android Vector Drawables:

```kotlin
// In Compose
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
import androidx.compose.ui.res.painterResource

@Composable
fun HomeIcon() {
    Image(
        painter = painterResource(id = R.drawable.ic_home),
        contentDescription = "Home"
    )
}

// Or using Icon component
import androidx.compose.material3.Icon

Icon(
    painter = painterResource(id = R.drawable.ic_home),
    contentDescription = "Home"
)
```

```xml
<!-- In XML layout -->
<ImageView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:src="@drawable/ic_home" />
```

## Available Sizes

Material Symbols are optimized for these sizes:
- **18px**: Small inline icons
- **20px**: Standard mobile icons
- **24px**: Default material icon size
- **36px**: Medium display icons
- **48px**: Large display icons

## Icon Naming Convention

When downloading icons:
- Use `ic_` prefix for icon files (e.g., `ic_home.xml`)
- Consider adding style suffix for non-default styles (e.g., `ic_home_rounded.xml`)
- Consider adding size suffix for non-standard sizes (e.g., `ic_home_48.xml`)
- Compose files are usually better with PascalCase filenames (e.g., `Home.kt`)
- Apple SVG assets can keep the icon name directly (e.g., `toggle_on.svg`)

## Notes

- The script caches metadata in the system temporary directory for faster subsequent searches
- Metadata is fetched from `http://fonts.google.com/metadata/icons`
- XML icons use the default Google asset URL for default axes and switch to the Google variant path `.../{icon}/{variant}/{size}px.xml` for custom `fill`, `weight`, or `grade`
- SVG icons use the default Google asset URL for default axes and switch to the Google variant path `.../{icon}/{variant}/{size}px.svg` for custom `fill`, `weight`, or `grade`
- Compose icons are downloaded from `https://fonts.gstatic.com/render/v1/Material+Symbols+{Style}/{size}dp/{icon}.kt?...`
- The `apple` format is a compatibility alias for the default SVG asset at `https://fonts.gstatic.com/s/i/short-term/release/{style}/{icon}/default/{size}px.svg`
- Use `--format svg` when you need custom `--fill`, `--weight`, or `--grade` with an SVG output
- The script uses only Python standard library modules and is portable across Linux, macOS, and Windows

## URL Pattern

Icons are downloaded using these patterns:
```
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/default/{size}px.xml
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/{variant_segments}/{size}px.xml
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/default/{size}px.svg
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/{variant_segments}/{size}px.svg
https://fonts.gstatic.com/render/v1/{compose_family}/{size}dp/{icon_name}.kt?var=opsz,wght,FILL,GRAD,ROND@{size},400,0,0,50
```

Where `style_folder` is one of:
- `materialsymbolsoutlined` (for outlined style)
- `materialsymbolsrounded` (for rounded style)
- `materialsymbolssharp` (for sharp style)

And `compose_family` is one of:
- `Material+Symbols+Outlined`
- `Material+Symbols+Rounded`
- `Material+Symbols+Sharp`

For XML and SVG variant folders:
- only non-default axis segments are included
- negative grades are encoded with `N`, for example `gradN25`
- examples: `fill1`, `wght700`, `grad200`, `wght700grad200fill1`
