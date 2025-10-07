from zenml import pipeline

from steps import feature_engineering as fe_steps


@pipeline
def feature_engineering(author_full_names: list[str], wait_for: str | list[str] | None = None) -> list[str]:

    """
    Feature Engineering Pipeline for RAG System
    
    This pipeline transforms raw repository documents into vector embeddings suitable
    for retrieval-augmented generation (RAG). It processes documents through cleaning,
    chunking, embedding, and vector database storage stages.
    
    Pipeline Flow:
    1. Query raw documents from MongoDB data warehouse
    2. Clean and normalize document content  
    3. Load cleaned documents to vector database
    4. Chunk documents and generate embeddings
    5. Load embedded chunks to vector database
    
    Args:
        author_full_names (list[str]): List of author names to filter repositories.
                                     Used to process documents from specific authors only.
        wait_for (str | list[str] | None, optional): Pipeline step(s) to wait for 
                                                   before starting execution. Enables
                                                   pipeline orchestration and dependencies.
    
    Returns:
        list[str]: List containing invocation IDs from the two vector database 
                  loading steps, useful for tracking pipeline execution and 
                  downstream dependencies.
    
    Pipeline Steps:
        - query_data_warehouse: Retrieves raw documents from MongoDB
        - clean_documents: Normalizes and cleans document content
        - load_to_vector_db (1st): Stores cleaned documents
        - chunk_and_embed: Splits documents into chunks and creates embeddings
        - load_to_vector_db (2nd): Stores embedded chunks for RAG retrieval
    
    Example:
        >>> pipeline_result = feature_engineering(
        ...     author_full_names=["Chris Morris"],
        ...     wait_for="data_extraction_pipeline"
        ... )
        >>> print(f"Pipeline completed with IDs: {pipeline_result}")
    """
    raw_documents = fe_steps.query_data_warehouse(author_full_names, after=wait_for)

    cleaned_documents = fe_steps.clean_documents(raw_documents)
    last_step_1 = fe_steps.load_to_vector_db(cleaned_documents)

    embedded_documents = fe_steps.chunk_and_embed(cleaned_documents)
    last_step_2 = fe_steps.load_to_vector_db(embedded_documents)

    return [last_step_1.invocation_id, last_step_2.invocation_id]
