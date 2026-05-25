---
name: google-icons
description: Download Material Symbols icons from Google Fonts as Android Vector Drawable XML. Search icons by name, multiple styles supported (outlined, rounded, sharp).
---

# Google Icons Skill

This skill provides tools to search and download Material Symbols icons from Google Fonts for Android development. Icons are downloaded directly as Android Vector Drawable XML format.

## Overview

Material Symbols are Google's modern icon set, available in three styles:
- **Outlined** (default): Thin strokes, minimalist design
- **Rounded**: Soft, rounded corners
- **Sharp**: Angular, precise edges

Icons are downloaded directly as **Android Vector Drawable XML**, ready to use in your project immediately.

## Quick Start

### Search for Icons
```bash
python .opencode/skills/google-icons/scripts/download_icon.py --search home
```

### Download an Icon
```bash
python .opencode/skills/google-icons/scripts/download_icon.py --name home --output app/src/main/res/drawable/ic_home.xml
```

## Script Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--search` | `-q` | Search icons by name (lists matching icons) | - |
| `--name` | `-n` | Icon name to download | - |
| `--style` | `-s` | Icon style: `outlined`, `rounded`, `sharp` | `outlined` |
| `--size` | `-sz` | Size in px: `18`, `20`, `24`, `36`, `48` | `24` |
| `--output` | `-o` | Output file path (default: `ic_<name>.xml`) | `./ic_<name>.xml` |
| `--refresh` | - | Force refresh metadata cache | `False` |

## Usage Examples

### Search Icons
```bash
# Find icons containing "home"
python .opencode/skills/google-icons/scripts/download_icon.py --search home

# Find icons containing "settings"
python .opencode/skills/google-icons/scripts/download_icon.py --search settings
```

### Download Icons (XML format - ready to use)

```bash
# Basic download (outlined, 24px) - produces XML
python .opencode/skills/google-icons/scripts/download_icon.py --name home --output app/src/main/res/drawable/ic_home.xml

# Rounded style
python .opencode/skills/google-icons/scripts/download_icon.py --name settings --style rounded --output app/src/main/res/drawable/ic_settings.xml

# Sharp style with custom size
python .opencode/skills/google-icons/scripts/download_icon.py --name delete --style sharp --size 48 --output app/src/main/res/drawable/ic_delete_48.xml

# Filled variant (uses filled=true in vector)
python .opencode/skills/google-icons/scripts/download_icon.py --name favorite --output app/src/main/res/drawable/ic_favorite.xml
```

## Using Downloaded Icons in Android

Icons are ready to use immediately as Android Vector Drawables:

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

When downloading icons for Android:
- Use `ic_` prefix for icon files (e.g., `ic_home.xml`)
- Consider adding style suffix for non-default styles (e.g., `ic_home_rounded.xml`)
- Consider adding size suffix for non-standard sizes (e.g., `ic_home_48.xml`)

## Notes

- The script caches metadata in `/tmp/opencode/google_icons_metadata.json` for faster subsequent searches
- Metadata is fetched from `http://fonts.google.com/metadata/icons`
- Icons are downloaded from `https://fonts.gstatic.com/s/i/short-term/release/{style}/{icon}/default/{size}px.xml`
- All downloaded icons are Android Vector Drawable XML format, ready to use immediately
- No conversion needed - icons work directly in Android projects

## URL Pattern

Icons are downloaded using this pattern:
```
https://fonts.gstatic.com/s/i/short-term/release/{style_folder}/{icon_name}/default/{size}px.xml
```

Where `style_folder` is one of:
- `materialsymbolsoutlined` (for outlined style)
- `materialsymbolsrounded` (for rounded style)
- `materialsymbolssharp` (for sharp style)
