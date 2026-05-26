# Google Icons Skills

[![skills.sh](https://skills.sh/b/yamixst/google-icons-skills)](https://skills.sh/yamixst/google-icons-skills)

Download Material Symbols icons from Google Fonts as Android XML, SVG, Compose Kotlin, or Apple symbol SVG.

## Install

```bash
npx skills@latest add yamixst/google-icons-skills
```

## Skill

- `google-icons`: Search and download Material Symbols in multiple output formats.

## Repository Layout

```text
SKILL.md
scripts/download_icon.py
```

## Supported Formats

- `xml`: Android Vector Drawable XML
- `svg`: Standard SVG asset
- `compose`: Kotlin `ImageVector`
- `apple`: Google `_symbol.svg` export

## Example Commands

```bash
python3 scripts/download_icon.py --search toggle_on
python3 scripts/download_icon.py --name toggle_on --format xml --output ic_toggle_on.xml
python3 scripts/download_icon.py --name toggle_on --format svg --fill 1 --weight 700 --grade 200 --output toggle_on.svg
python3 scripts/download_icon.py --name toggle_on --format compose --fill 1 --weight 700 --grade 200 --output ToggleOn.kt
python3 scripts/download_icon.py --name toggle_on --format apple --fill 1 --grade 200 --output toggle_on_symbol.svg
```

## Notes

- Works on Linux, macOS, and Windows.
- Uses only the Python standard library.
- Skill instructions live in `SKILL.md` for agent consumption.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
