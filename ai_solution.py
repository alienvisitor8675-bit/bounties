```yaml
# Intent YAML
name: URL_CONTENT_EXTRACTION
description: Extracts the main content from a given web page URL.
family: CONTENT
---
# URL_CONTENT_EXTRACTION miner YAML
name: URL_CONTENT_EXTRACTION
version: 1.0
description: Extracts the main content from a given web page URL.
family: CONTENT
mining:
  - url_content_extraction:
      input:
        type: string
        required: true
        description: The URL to extract content from.
      output:
        type: object
        properties:
          url:
            type: string
            description: The input URL.
          title:
            type: string
            description: The title of the page.
          description:
            type: string
            description: The meta description of the page.
          content:
            type: string
            description: The main content of the page, extracted from the main text area or equivalent.
      processing:
        steps:
          - Extract the title from the page.
          - Extract the meta description from the page.
          - Extract the main content, focusing on the main text and ignoring sidebars and footers.
```