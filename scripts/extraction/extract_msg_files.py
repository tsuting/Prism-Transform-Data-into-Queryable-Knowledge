"""
Email extraction for .msg files using python-oxmsg (MIT licensed).

Uses python-oxmsg (MIT licensed) maintained by scanny (author of python-pptx, python-docx).
https://github.com/scanny/python-oxmsg
"""
from pathlib import Path
import re
import html as html_module
from oxmsg import Message
from scripts.logging_config import get_logger

logger = get_logger(__name__)


def format_email_as_markdown(msg_path: Path) -> str:
    """
    Extract and format .msg file as markdown.

    Args:
        msg_path: Path to .msg file

    Returns:
        Formatted markdown string
    """
    try:
        msg = Message.load(str(msg_path))

        markdown = []

        # Header
        markdown.append(f"# Email: {msg.subject or 'No Subject'}")
        markdown.append("")

        # Metadata
        markdown.append("## Email Metadata")
        markdown.append("")
        markdown.append(f"**From:** {msg.sender or 'Unknown'}")

        # To/CC accessed via message_headers dict
        headers = msg.message_headers or {}
        to_addr = headers.get('To', 'Unknown')
        cc_addr = headers.get('Cc')

        markdown.append(f"**To:** {to_addr}")
        if cc_addr:
            markdown.append(f"**CC:** {cc_addr}")
        if msg.sent_date:
            markdown.append(f"**Date:** {msg.sent_date}")
        markdown.append("")

        # Attachments
        if msg.attachments:
            markdown.append("## Attachments")
            markdown.append("")
            for i, attachment in enumerate(msg.attachments, 1):
                name = attachment.file_name or f'attachment_{i}'
                size = attachment.size or 0
                markdown.append(f"{i}. **{name}** ({size:,} bytes)")
            markdown.append("")

        # Body - try plain text first, fall back to HTML
        markdown.append("## Email Body")
        markdown.append("")

        body = msg.body
        if not body and msg.html_body:
            # Convert HTML to plain text
            html = msg.html_body
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<[^>]+>', ' ', html)
            html = html_module.unescape(html)
            body = re.sub(r'\s+', ' ', html).strip()

        if body:
            markdown.append(body.strip())
        else:
            markdown.append("*[No body content]*")
        markdown.append("")

        result = "\n".join(markdown)

        size_kb = len(result.encode('utf-8')) / 1024
        logger.info(f"Extracted {msg_path.name}: {size_kb:.1f} KB")

        return result

    except Exception as e:
        logger.error(f"Failed to extract {msg_path.name}: {e}")
        return None
