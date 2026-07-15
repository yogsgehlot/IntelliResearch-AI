class ContextBuilder:

    @staticmethod
    def build(chunks):

        context = []

        for chunk in chunks:

            context.append(
                chunk["content"]
            )

        return "\n\n".join(context)