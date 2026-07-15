class CitationBuilder:
    @staticmethod
    def build(documents: list,):
        citations = []
        for doc in documents:
            citations.append(
                {
                    "document_id": doc["document_id"],
                    "chunk": doc["chunk_index"],
                }
            )

        return citations