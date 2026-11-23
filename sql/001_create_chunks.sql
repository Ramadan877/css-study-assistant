CREATE TABLE chunks (
    document_id TEXT NOT NULL,
    chunk_number INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    source_url TEXT NOT NULL,
    text TEXT NOT NULL,
    embedding_deployment TEXT NOT NULL,
    embedding vector(1536) NOT NULL,

    PRIMARY KEY (document_id, chunk_number)   
);