from bs4 import BeautifulSoup


def estimate_tokens(text):
    # Rough estimation: 1 token ≈ 4 characters
    return len(text) // 4


def chunk_dom_sections(dom_sections, max_tokens=2000):
    chunks = []
    current_chunk = ""
    current_token_count = 0

    for section in dom_sections:
        # Add metadata about the section
        section_info = (
            f"Similarity: {section['similarity']:.4f}\nClass: {section['class']}\n\n"
        )
        section_html = section["html"]

        # If adding this section would exceed the token limit, start a new chunk
        if estimate_tokens(current_chunk + section_info + section_html) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = ""
            current_token_count = 0

        # Add section info to the chunk
        current_chunk += section_info
        current_token_count += estimate_tokens(section_info)

        # Parse the HTML and add elements one by one
        soup = BeautifulSoup(section_html, "html.parser")
        for element in soup.recursiveChildGenerator():
            if isinstance(element, str) and element.strip():
                # Text node
                text = element.strip()
                if estimate_tokens(current_chunk + text + "\n") > max_tokens:
                    chunks.append(current_chunk.strip())
                    current_chunk = section_info  # Start new chunk with section info
                    current_token_count = estimate_tokens(section_info)
                current_chunk += text + "\n"
                current_token_count += estimate_tokens(text + "\n")
            elif element.name:
                # Element node
                opening_tag = str(element.name)
                if element.attrs:
                    attrs = " ".join(f'{k}="{v}"' for k, v in element.attrs.items())
                    opening_tag += f" {attrs}"
                if estimate_tokens(current_chunk + f"<{opening_tag}>\n") > max_tokens:
                    chunks.append(current_chunk.strip())
                    current_chunk = section_info  # Start new chunk with section info
                    current_token_count = estimate_tokens(section_info)
                current_chunk += f"<{opening_tag}>\n"
                current_token_count += estimate_tokens(f"<{opening_tag}>\n")

        current_chunk += "\n"  # Add a separator between sections

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
