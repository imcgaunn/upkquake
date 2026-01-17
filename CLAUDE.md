# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

upkquake is a Python tool that extracts and prepares Quake II retail CD data for use with modern Quake II clients (like Yamagi Quake). It downloads a Quake II CD image from archive.org, splits the bin/cue files into data and audio tracks, and converts the audio to OGG format.

The tool is invoked via the `upkq` command-line script.

## Development Commands

Tasks are defined in `mise.toml` and run via `mise run <task>`.

### Initial Setup
```bash
mise run init
# or directly: uv sync
```

### Testing
```bash
# Run all tests
mise run test

# Run a single test file
uv run pytest -s tests/test_extraction.py

# Run a specific test
uv run pytest -s tests/test_extraction.py::test_function_name
```

### Code Quality
```bash
# Format code with black
mise run format

# Lint code with flake8
mise run lint

# Pre-commit hooks (black)
pre-commit run --all-files
```

### Cleanup
```bash
mise run clean  # Remove build artifacts, .venv, and __pycache__
```

## Architecture

### Module Responsibilities

**upkquake.py** (main entry point)
- Orchestrates the entire workflow from download to conversion
- Sets up logging with rich handlers
- Called via the `upkq` console script (defined in pyproject.toml)

**assets.py** (asset management)
- Manages downloading of external assets (Quake II archive, Yamagi patch)
- Implements checksum verification and caching
- ALL assets list defines all downloadable assets with URLs, checksums, and output paths

**extraction.py** (CD extraction and conversion)
- Extracts zip files using 7z
- Splits bin/cue CD images into data track (ISO) and audio tracks (CDR) using bchunk
- Converts CDR audio tracks to OGG using sox
- **Important**: The `-s` flag for bchunk switches endianness - without it, audio sounds like static

**util.py** (utilities)
- File hashing with chunked reading for large files
- File downloading with streaming
- Directory creation helpers

**constants.py** (configuration)
- URLs and SHA256 checksums for all external assets
- Cache directory paths (defaults to ~/.cache/upkquake)
- Chunk sizes for hashing and downloading

### Data Flow

1. Main downloads assets (Quake II zip, Yamagi patch) with caching/verification
2. Zip is extracted and bin/cue files are identified
3. bchunk splits the CD image into data track (ISO) and audio tracks (CDR files)
4. Sox converts each CDR file to numbered OGG files (e.g., 02.ogg for track 2)
5. Output goes to generated_qbase2 directory (can be renamed to baseq2 for use with Quake II clients)

### External Dependencies

The tool requires these system binaries to be installed:
- `7z` - for extracting zip and ISO files
- `bchunk` - for splitting bin/cue CD images
- `sox` - for audio conversion to OGG
- `vorbis-tools` - for OGG encoding support

## Key Implementation Details

- All subprocess calls use `check=True` to ensure errors are caught
- Files are processed in the cache directory (~/.cache/upkquake) by default
- The endianness flag (`-s`) in bchunk is critical for proper audio extraction
- Track numbering is extracted from filenames via regex: `iso(\d{2})\.cdr`
- Asset verification uses SHA256 checksums with chunked reading for efficiency

## Known TODOs

Per the README and code comments:
- Add proper CLI interface for specifying output file locations
- Move files into final proper structure (currently manual step)
- Optional cleanup of unnecessary files from ISO extraction
