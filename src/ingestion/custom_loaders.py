import json
from langchain_community.document_loaders import NotebookLoader
# --- FIX: Updated Import from 'langchain.schema' to 'langchain_core.documents' ---
from langchain_core.documents import Document

class CleanNotebookLoader(NotebookLoader):
    """
    A Custom Loader that cleans .ipynb files by:
    1. Removing code output (logs, errors, graphs)
    2. Only keeping Markdown text and Raw Code
    """
    def load(self):
        """
        Overriding the load method to ensure outputs are stripped
        before LangChain processes them.
        """
        try:
            # We enforce include_outputs=False to reduce noise
            loader = NotebookLoader(
                self.file_path,
                include_outputs=False,
                max_output_length=0,
                remove_newline=True,
                traceback=False
            )
            return loader.load()
        except Exception as e:
            print(f"⚠️ Warning: Could not parse notebook {self.file_path}. Error: {e}")
            return []