import fitz
from pathlib import Path
from typing import List, Dict

from config import PDF_DIR, PROCESSED_DIR
from utils import save_pickle, clean_text
from .base import BaseDataSource
from components.storage.supabase import SupabaseStorage


class PDFDataSource(BaseDataSource):
    """Data source for PDF files."""

    def __init__(self, pdf_dir: Path = PDF_DIR):
        """
        Initialize PDF data source.

        Args:
            pdf_dir: Directory containing PDF files
        """
        self.pdf_dir = Path(pdf_dir)
        self.pickle_dir = PROCESSED_DIR / "pickle"
        self.txt_dir = PROCESSED_DIR / "txt"
        self.supabase = SupabaseStorage()

    def sync(self, prefix: str = "", overwrite: bool = True) -> None:
        """
        Sync PDFs from cloud storage to local directory.
        
        Args:
            prefix: Optional prefix to filter files in bucket
            overwrite: Whether to overwrite existing local files
        """
        print("Syncing with cloud storage...")
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.supabase.download(
            remote_path=None,
            local_path=self.pdf_dir,
            prefix=prefix,
            overwrite=overwrite
        )

    def extract_text_with_metadata(self, pdf_path: Path) -> List[Dict]:
        """
        Extract text from each page of a PDF and clean it.

        Returns:
            List of dictionaries with page number and cleaned text
        """
        page_data = []
        with fitz.open(pdf_path) as doc:
            for page_number, page in enumerate(doc, start=1):
                raw_text = page.get_text()
                cleaned_text = clean_text(raw_text)
                if cleaned_text.strip():
                    page_data.append({
                        "page_number": page_number,
                        "text": cleaned_text
                    })
        return page_data

    def load(self) -> List[Dict]:
        """Load and extract text from all PDFs in the directory."""
        all_pages = []
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        
        for pdf_file in pdf_files:
            pages = self.extract_text_with_metadata(pdf_file)
            all_pages.extend(pages)
        
        return all_pages

    def process(self, save_txt: bool = True) -> None:
        """
        Process all PDFs in pdf_dir:
        - Save pickled page-level metadata in PROCESSED_DIR/pickle/
        - Optionally save human-readable .txt in PROCESSED_DIR/txt/
        
        Note: Call sync() before process() to download latest files from cloud.
        """
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("No PDF files found to process")
            return
        
        # Create output folders
        self.pickle_dir.mkdir(parents=True, exist_ok=True)
        self.txt_dir.mkdir(parents=True, exist_ok=True)

        print(f"Processing {len(pdf_files)} PDF(s)...")

        for pdf_file in pdf_files:
            pages = self.extract_text_with_metadata(pdf_file)

            if not pages:
                continue

            # Save pickled object
            save_pickle(
                directory=self.pickle_dir,
                data=pages,
                filename=f"{pdf_file.stem}.pkl"
            )

            # Optionally save human-readable text file
            if save_txt:
                full_text = "\n\n".join(
                    f"[Page {p['page_number']}]\n{p['text']}" for p in pages
                )
                txt_file = self.txt_dir / f"{pdf_file.stem}.txt"
                txt_file.write_text(full_text, encoding="utf-8")

        print(f"✓ Processed {len(pdf_files)} PDF(s)")


def process_all_pdfs(save_txt: bool = True) -> None:
    """Convenience function to process all PDFs."""
    pdf_source = PDFDataSource()
    pdf_source.sync()  # Sync with cloud first
    pdf_source.process(save_txt=save_txt)


if __name__ == "__main__":
    process_all_pdfs(save_txt=True)