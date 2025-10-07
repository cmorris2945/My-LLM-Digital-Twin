from zenml import pipeline
from steps.feature_engineering.query_data_warehouse import query_data_warehouse

@pipeline
def test_query_pipeline():
    """Test pipeline to check the query step and metadata"""
    # Use the actual user name from the database
    author_names = ["Chris Morris"]
    
    raw_documents = query_data_warehouse(author_names)
    return raw_documents

if __name__ == "__main__":
    # Run the pipeline
    test_query_pipeline()
