class MarkdownFormatter:

    @staticmethod
    def clean(markdown: str):

        markdown = markdown.strip()

        markdown = markdown.replace("\r\n", "\n")

        return markdown