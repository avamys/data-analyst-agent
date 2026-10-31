"""Centralized Jinja2 template management for prompts"""

import logging
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


class PromptTemplateManager:
    """
    Manages Jinja2 templates for agent prompts

    Benefits over embedded Python strings:
    - Clean separation of prompt content from code
    - Syntax highlighting for prompts in editors
    - Easy for non-developers to edit
    - Clean version control diffs
    - Template inheritance and reuse
    - Conditional logic and filters

    Usage:
        from agent.prompts.template_manager import prompt_templates

        prompt = prompt_templates.render(
            "orchestrator/strategy_selection.jinja2",
            profile_summary=profile_summary,
            dataset_info=dataset_info
        )
    """

    _instance: Optional["PromptTemplateManager"] = None

    def __new__(cls):
        """Singleton pattern to cache Jinja2 environment"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize Jinja2 environment (only once)"""
        if self._initialized:
            return

        # Template directory is agent/templates/
        template_dir = Path(__file__).parent.parent / "templates"

        if not template_dir.exists():
            raise RuntimeError(
                f"Template directory not found: {template_dir}\n"
                f"Please ensure agent/templates/ exists with prompt templates."
            )

        # Create Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),  # Don't autoescape text
            trim_blocks=True,  # Remove first newline after block
            lstrip_blocks=True,  # Strip leading spaces from blocks
            keep_trailing_newline=True,  # Preserve final newline
        )

        # Register custom filters
        self._register_filters()

        self._initialized = True
        logger.info(
            f"PromptTemplateManager initialized with templates from: {template_dir}"
        )

    def _register_filters(self):
        """Register custom Jinja2 filters for prompt formatting"""

        # Number formatting filter
        def number_format(value, decimals=0):
            """Format number with thousands separator"""
            if isinstance(value, (int, float)):
                if decimals > 0:
                    return f"{value:,.{decimals}f}"
                return f"{value:,}"
            return str(value)

        # Percentage filter
        def percentage(value, decimals=1):
            """Format as percentage"""
            if isinstance(value, (int, float)):
                return f"{value * 100:.{decimals}f}%"
            return str(value)

        # Default value filter (if empty/None)
        def default_value(value, default="None"):
            """Return default if value is None or empty"""
            if value is None or (isinstance(value, str) and not value.strip()):
                return default
            return value

        # Truncate long text
        def truncate_text(value, length=100, suffix="..."):
            """Truncate text to max length"""
            if isinstance(value, str) and len(value) > length:
                return value[:length] + suffix
            return value

        # Register filters
        self.env.filters["number_format"] = number_format
        self.env.filters["percentage"] = percentage
        self.env.filters["default"] = default_value
        self.env.filters["truncate"] = truncate_text

    def render(self, template_path: str, **context) -> str:
        """
        Render template with context variables

        Args:
            template_path: Path to template relative to agent/templates/
                          e.g., "orchestrator/strategy_selection.jinja2"
            **context: Variables to pass to template

        Returns:
            Rendered prompt string

        Example:
            prompt = prompt_templates.render(
                "specialists/eda_analysis.jinja2",
                task_description="Analyze correlations",
                dataset_path="data/titanic.csv",
                n_rows=891
            )
        """
        try:
            template = self.env.get_template(template_path)
            rendered = template.render(**context)
            logger.debug(f"Rendered template: {template_path} ({len(rendered)} chars)")
            return rendered
        except Exception as e:
            logger.error(
                f"Failed to render template {template_path}: {e}", exc_info=True
            )
            raise RuntimeError(
                f"Template rendering failed for '{template_path}': {e}"
            ) from e

    def list_templates(self) -> list[str]:
        """List all available templates"""
        return self.env.list_templates()


# Singleton instance for easy importing
prompt_templates = PromptTemplateManager()
