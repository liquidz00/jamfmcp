"""Custom Sphinx directive for styling AI prompts as chat input boxes."""

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

logger = logging.getLogger(__name__)


class ai_prompt(nodes.General, nodes.Element):
    """Node for AI prompt boxes."""
    pass


def visit_ai_prompt_html(self, node):
    """Generate opening HTML for AI prompt."""
    # Get the text content directly
    text = node.astext()
    self.body.append(
        f'<div class="ai-prompt-box">'
        f'<div class="ai-prompt-input">{self.encode(text)}</div>'
        f'</div>'
    )
    # Skip children since we already rendered the text
    raise nodes.SkipNode


class AIPromptDirective(SphinxDirective):
    """
    Directive to create styled AI prompt input boxes.

    Usage in Markdown (MyST):
        :::{ai-prompt}
        Get the health scorecard for computer with serial number ABC123
        :::

    Usage in reStructuredText:
        .. ai-prompt::

           Get the health scorecard for computer with serial number ABC123
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        # Create container node
        node = ai_prompt()

        # Store the raw text content
        text = '\n'.join(self.content)
        node += nodes.Text(text)

        return [node]


def setup(app: Sphinx):
    """Register the extension with Sphinx."""

    # Add the node and directive
    app.add_node(
        ai_prompt,
        html=(visit_ai_prompt_html, None)  # No depart function needed
    )
    app.add_directive('ai-prompt', AIPromptDirective)

    # Add CSS file
    app.add_css_file('ai-prompt.css')

    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
