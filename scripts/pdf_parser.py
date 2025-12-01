"""
PDF Parser Script using LlamaParse

A clean, modular script for parsing PDF files with proper separation of concerns,
error handling, and configuration management.

Usage:
    export LLAMA_CLOUD_API_KEY='your-api-key'
    python pdf_parser.py
"""

import json
import os
from typing import Dict, List, Any, Tuple

from llama_cloud_services import LlamaParse

from config import ParserSettings, PathSettings, load_settings_from_env, get_default_paths
from biology_textbook import get_chapter_and_lecture_by_page


class PDFParser:
    """Main PDF Parser class with clean separation of concerns"""
    
    def __init__(self, settings: ParserSettings):
        """
        Initialize PDF Parser with settings
        
        Args:
            settings: ParserSettings instance with parsing configuration
        """
        self.settings = settings
        self._text_parser = None
        self._image_parser = None
    
    def _create_text_parser(self) -> LlamaParse:
        """Create text parser instance with configuration"""
        return LlamaParse(
            api_key=self.settings.api_key,
            max_pages=self.settings.max_pages,
            parse_mode=self.settings.parse_mode_text,
            model=self.settings.model,
            high_res_ocr=self.settings.high_res_ocr,
            adaptive_long_table=self.settings.adaptive_long_table,
            outlined_table_extraction=self.settings.outlined_table_extraction,
            output_tables_as_HTML=self.settings.output_tables_as_html,
            precise_bounding_box=self.settings.precise_bounding_box,
            system_prompt_append=self.settings.system_prompt,
            replace_failed_page_mode=self.settings.replace_failed_page_mode,
        )
    
    def _create_image_parser(self) -> LlamaParse:
        """Create image parser instance with configuration"""
        return LlamaParse(
            api_key=self.settings.api_key,
            max_pages=self.settings.max_pages,
            parse_mode=self.settings.parse_mode_image,
            high_res_ocr=self.settings.high_res_ocr,
            adaptive_long_table=self.settings.adaptive_long_table,
            outlined_table_extraction=self.settings.outlined_table_extraction,
            output_tables_as_HTML=self.settings.output_tables_as_html,
            precise_bounding_box=self.settings.precise_bounding_box,
            page_separator=self.settings.page_separator,
            system_prompt_append=self.settings.system_prompt,
            replace_failed_page_mode=self.settings.replace_failed_page_mode,
        )
    
    def parse_pdf(self, pdf_path: str) -> Tuple[Any, Any]:
        """
        Parse PDF file and extract text and images
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (text_result, image_result)
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"📄 Parsing PDF: {pdf_path}")
        
        # Create parsers
        text_parser = self._create_text_parser()
        image_parser = self._create_image_parser()
        
        # Parse PDF
        print("  ⏳ Extracting text content...")
        text_result = text_parser.parse(pdf_path)
        
        print("  ⏳ Extracting images...")
        image_result = image_parser.parse(pdf_path)
        
        print("  ✓ PDF parsed successfully")
        return text_result, image_result
    
    def extract_markdown(self, text_result, output_path: str) -> None:
        """
        Extract and save markdown documents
        
        Args:
            text_result: Result from text parser
            output_path: Path to save markdown file
        """
        print(f"📝 Extracting markdown...")
        markdown_documents = text_result.get_markdown_documents(split_by_page=True)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            for doc in markdown_documents:
                f.write(doc.text)
                f.write("\n\n")
        
        print(f"  ✓ Saved: {output_path}")
    
    def extract_images(
        self, 
        image_result, 
        image_dir: str,
        include_screenshots: bool = True,
        include_objects: bool = True
    ) -> List[Any]:
        """
        Extract and save images from PDF
        
        Args:
            image_result: Result from image parser
            image_dir: Directory to save images
            include_screenshots: Include screenshot images
            include_objects: Include object images
            
        Returns:
            List of image documents
        """
        print(f"🖼️  Extracting images...")
        os.makedirs(image_dir, exist_ok=True)
        
        image_documents = image_result.get_image_documents(
            include_screenshot_images=include_screenshots,
            include_object_images=include_objects,
            image_download_dir=image_dir,
        )
        
        print(f"  ✓ Extracted {len(image_documents)} images to: {image_dir}")
        return image_documents
    
    def build_json_result(self, text_result, image_documents: List[Any]) -> Dict[str, Any]:
        """
        Build structured JSON result from parsing results
        
        Args:
            text_result: Result from text parser
            image_documents: List of extracted image documents
            
        Returns:
            Dictionary with structured page data including chapter and lecture info
        """
        print("🔧 Building JSON result...")
        json_result = {"pages": {}}
        
        for i, page in enumerate(text_result.pages, 1):
            page_images = self._extract_page_images(image_documents, i)
            
            # Get chapter and lecture information for this page
            chapter_lecture_info = get_chapter_and_lecture_by_page(i)
    
            page_data = {
                "page": i,
                "text": page.text,
                "md": page.md,
                "images": page_images,
                "layout": str(page.layout) if hasattr(page, 'layout') else None,
                        "structuredData": page.structuredData if hasattr(page, 'structuredData') else None,
                        "chapter": chapter_lecture_info["chapter"] if chapter_lecture_info else None,
                        "lecture": chapter_lecture_info["lecture"] if chapter_lecture_info else None
            }
            json_result["pages"][str(i)] = page_data

        print(f"  ✓ Processed {len(text_result.pages)} pages")
        return json_result
    
    def _extract_page_images(self, image_documents: List[Any], page_number: int) -> List[Dict[str, Any]]:
        """
        Extract images for a specific page
        
        Args:
            image_documents: List of all image documents
            page_number: Page number to extract images for
            
        Returns:
            List of image dictionaries for the page
        """
        page_images = []
        for img_doc in image_documents:
            if hasattr(img_doc, 'metadata') and img_doc.metadata.get('page_number') == page_number:
                page_images.append({
                    "image_path": getattr(img_doc, 'image_path', None),
                    "image_url": getattr(img_doc, 'image_url', None),
                    "text": getattr(img_doc, 'text', None)
                })
        return page_images
    
    def save_json_result(self, json_result: Dict[str, Any], output_path: str) -> None:
        """
        Save JSON result to file
        
        Args:
            json_result: Dictionary to save
            output_path: Path to save JSON file
        """
        print(f"💾 Saving JSON result...")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_result, f, ensure_ascii=False, indent=2)
            print(f"  ✓ Saved: {output_path}")


def run_parser(settings: ParserSettings, paths: PathSettings) -> None:
    """
    Run the PDF parser with given settings
    
    Args:
        settings: Parser settings
        paths: Path settings for input/output files
    """
    # Initialize parser
    parser = PDFParser(settings)
    
    # Parse PDF
    text_result, image_result = parser.parse_pdf(paths.input_pdf)
    
    # Extract markdown
    parser.extract_markdown(text_result, paths.output_markdown)
    
    # Extract images
    image_documents = parser.extract_images(image_result, paths.output_images_dir)
    
    # Build and save JSON result
    json_result = parser.build_json_result(text_result, image_documents)
    parser.save_json_result(json_result, paths.output_json)


def main():
    """Main execution function"""
    print("=" * 60)
    print("PDF Parser using LlamaParse")
    print("=" * 60)
    print()
    
    try:
        # Load settings from environment
        settings = load_settings_from_env()
        paths = get_default_paths()
        
        # Run parser
        run_parser(settings, paths)
        
        print()
        print("=" * 60)
        print("✓ All tasks completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n❌ File Error: {e}")
        print("   Make sure 'input.pdf' exists in the scripts directory")
        raise
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        raise
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("   Check your configuration and try again")
        raise


if __name__ == "__main__":
    main()
