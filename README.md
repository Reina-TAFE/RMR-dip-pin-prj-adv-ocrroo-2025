# Overview

Include a brief overview of the project, include:

- How do you deploy and run the project?
1. Clone the Repo
> ```bash
> git clone https://github.com/Reina-TAFE/RMR-dip-pin-prj-adv-ocrroo-2025.git
> ```

2. Install uv (Globally)
> ```bash
> pip install uv
> ```

3. Generate virtual environment from pyproject.toml
> cd into project directory
> ```bash
> cd RMR-dip-pin-prj-adv-ocrroo-2025/
> ```
> 
> use uv to automatically generate venv with project dependencies
> ```bash
> uv sync --python 3.13
> ```

4. Install TerreractOCR application
> Go to tesseract website and install TesseractOCR
> [Tesseract](https://github.com/UB-Mannheim/tesseract/releases)

5. Add terreract.exe path to library_basics
> Go to preliminary/library_basics.py
> Update TESS_PATH with absolute path to your TesseractOCR executable (tesseract.exe) 

6. Start FastAPI
> use uv to run FastAPI
> ```bash
> uv run fastapi dev back-end/simple_api.py
> ```

7. Run commands
> Use curl to run commands using provided endpoints
> ```bash
> curl 127.0.0.1:8000/video/demo
> ```


- What are its core dependencies?
> Tesseract OCR executable. (required by pytesseract wrapper library)
> Pytesseract
> OpenCV
> FastAPI
> Flask

- Who is it for and why?
> This application is intended for vision impaired students to be able to transcribe text from videos
> in order to allow them to utilise video resources where on-screen text is not reflected in the audio.
> This application can provide a text transcript of any on-screen text that can be read aloud using external
> screen-reading or text-to-speech tools.
