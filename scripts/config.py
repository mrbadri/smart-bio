"""
Configuration module for PDF Parser

Centralized configuration management with validation and defaults.
"""

import os
from typing import Optional
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path)


@dataclass
class ParserSettings:
    """Parser configuration settings"""
    
    # API Configuration
    api_key: str
    
    # Parsing Settings
    max_pages: int = 25
    parse_mode_text: str = "parse_page_with_agent"
    parse_mode_image: str = "parse_page_with_llm"
    model: str = "openai-gpt-4-1-mini"
    
    # OCR Settings
    high_res_ocr: bool = True
    
    # Table Settings
    adaptive_long_table: bool = True
    outlined_table_extraction: bool = True
    output_tables_as_html: bool = True
    
    # Advanced Settings
    precise_bounding_box: bool = True
    page_separator: str = "\n\n---\n\n"
    replace_failed_page_mode: str = "raw_text"
    
    # System Prompt
    system_prompt: str = field(default=(
        "Only extract images that are non-text figures (photos, diagrams, charts). "
        "If a region contains mostly text (Persian/Arabic/English), do NOT treat it as an image; "
        "OCR it as text instead. Never output an image for pure text blocks."
    ))
    
    # Language Settings (optional)
    languages: Optional[list] = None


@dataclass
class OpenAISettings:
    """OpenAI API configuration settings"""
    
    # API Configuration
    api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"


@dataclass
class PathSettings:
    """File path settings"""
    
    input_pdf: str = "./input.pdf"
    output_markdown: str = "./out/output.md"
    output_json: str = "./out/output.json"
    output_images_dir: str = "./out/images"


def load_settings_from_env() -> ParserSettings:
    """
    Load parser settings from environment variables or .env file
    
    Returns:
        ParserSettings instance with values from environment
        
    Raises:
        ValueError: If required environment variables are missing
    """
    api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not api_key:
        raise ValueError(
            "LLAMA_CLOUD_API_KEY not found. "
            "Either:\n"
            "  1. Create a .env file: cp env.example .env (and add your key)\n"
            "  2. Export it: export LLAMA_CLOUD_API_KEY='your-api-key'"
        )
    
    return ParserSettings(
        api_key=api_key,
        max_pages=int(os.getenv("MAX_PAGES", "25")),
        high_res_ocr=os.getenv("HIGH_RES_OCR", "true").lower() == "true",
    )


def get_default_paths() -> PathSettings:
    """Get default path settings"""
    return PathSettings()


def load_openai_settings() -> OpenAISettings:
    """
    Load OpenAI settings from environment variables or .env file
    
    Returns:
        OpenAISettings instance with values from environment
        
    Raises:
        ValueError: If required environment variables are missing
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Either:\n"
            "  1. Create a .env file: cp env.example .env (and add your key)\n"
            "  2. Export it: export OPENAI_API_KEY='your-api-key'"
        )
    
    return OpenAISettings(
        api_key=api_key,
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
    )

