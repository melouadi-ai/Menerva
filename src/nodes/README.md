# Nodes — Pipeline Stage Implementations

This package contains the individual processing stages of the Menerva MAS pipeline.

## Stage Overview

| Stage | Module | Status | Description |
|---|---|---|---|
| 1 | `ingestion.py` | ⏳ TODO | Open file, verify readability, extract metadata |
| 2 | `splitter.py` | ⏳ TODO | PDF → page images, Excel → rows |
| 3 | `classifier.py` | ⏳ TODO | VLM classifies content type per page |
| 4 | `extractor.py` | ⏳ TODO | VLM extracts JSON intermediate |
| 5 | `validator.py` | ⏳ TODO | Pydantic validates JSON schema |
| 6 | `transformer.py` | ⏳ TODO | Python transforms to ADAS format |
| 7 | `merger.py` | ⏳ TODO | Merge stations, compute hex, renumber IDs |

## Node Interface

Each node must implement the following interface:

```python
from typing import Any

class BaseNode:
    name: str
    
    def run(self, input_data: Any, config: dict | None = None) -> Any:
        """Process input and return output for next stage."""
        raise NotImplementedError
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input before processing."""
        return True
```

## Running a Single Node

```python
from src.nodes.splitter import PDFSplitter

node = PDFSplitter()
result = node.run("path/to/document.pdf", {"output_dir": "tmp/pages/"})
```

## Chain Runner

The chain runner (`run_pipeline.py`) will execute all 7 nodes in sequence:

```bash
python -m src.run_pipeline --input document.pdf --output output.json
```
