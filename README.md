# Scraping and Chunking experiments

1. Scraped the entire Notion help center knowledge base:
   - Used Python with BeautifulSoup to implement the scraper
   - Collected all Help Articles from https://www.notion.so/help

2. Extracted core text content from each article

3. Split articles into smaller chunks:
   - Explored four different chunking strategies for RAG-type applications:
     1. RecursiveTokenChunker: Recursively splits text based on token count
     2. ClusterSemanticChunker: Uses semantic similarity to cluster text
     3. KamradtModifiedChunker: A modified version of Kamradt's chunking algorithm
     4. NaiveChunker: Simple character-based chunking
   - Implemented an LLMChunker as a fifth strategy
   - Evaluated each strategy based on precision, recall, and IOU metrics
   - Produced arrays of chunks as the final output for each strategy

---

# Results

Evaluation Results Summary:
| Chunker | Precision Mean | Recall Mean | IOU Mean |
|---------|----------------|-------------|----------|
| RecursiveTokenChunker | 0.0135 | 0.7358 | 0.0135 |
| ClusterSemanticChunker | 0.0327 | 0.6862 | 0.0325 |
| KamradtModifiedChunker | 0.0230 | 0.7293 | 0.0230 |
| NaiveChunker | 0.0367 | 0.6450 | 0.0363 |
| LLMSemanticChunker | 0.0357 | 0.7043 | 0.0357 |

---

# Usage

To use this project, follow these steps:

1. **Setup:**
   - Clone the repository:
     ```
     git clone https://github.com/chirag9127/chunking_expt.git
     cd chunking_expt
     ```
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

2. **Scraping:**
   - Run the scraper to collect articles from the Notion help center:
     ```
     python scraper.py
     ```
   - This will save the scraped articles in a checkpoint file.

3. **Chunking:**
   - To chunk the articles using the LLMChunker:
     ```
     python chunker.py
     ```
   - This will process the articles from the checkpoint file and create chunks.

4. **Evaluation:**
   - To evaluate different chunking strategies:
     ```
     python eval.py
     ```
   - This will run the evaluation on different chunking methods and output the results.

5. **Viewing Results:**
   - The evaluation results will be saved in `chunker_evaluation_results.json`.
   - You can also find a summary of the results at the end of this README.

Note: Make sure to set up your OpenAI API key in a `.env` file or as an environment variable before running the LLMChunker.

