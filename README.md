# Scraping and Chunking: Mini Project

Your goal for this project is to scrape an entire public-hosted knowledge base and chunk it effectively into clean smaller pieces so that related content is preserved in a single chunk.

## Considerations:

- Please implement this solution in Python. We recommend using `BeautifulSoup`.
- The priorities in descending order are:
    1. Cleanliness/organization of the code - **SIMPLER IS BETTER**
    2. Correctness
    3. Creativity
- This project is not timed and you may use the internet and LLM helpers as you wish.
- When finished, share your Github repo with `ashwinsr` and `emptycrown`.

## Step 1

First, scrape all the Help Articles from the [**Notion help center**](https://www.notion.so/help). Make sure you get every page and all the relevant content from that page. Feel free to ignore any guides in Notion Academy.

## Step 2

Extract the core text content from each article. Feel free to ignore images, other media, and any components that are not directly related to the core article. Make sure to include all titles, notes, and paragraphs.

## Step 3

Now it's time to split the articles into smaller chunks. This is important for any RAG-type system. Make sure to keep headers and paragraphs together and don't break up bulleted lists mid-list. Your chunks should be roughly 750 characters or fewer but could be more if it's necessary to keep related context together.

> 💡 **Tip:** LLMs are very good at processing unstructured text (or HTML) and extracting what you want

Your final output should be an array of these chunks!

## Bonus

The text output of web scraping is often very messy. In particular, if there are tables, lists, or other unusual formatting, just converting HTML to text can look very odd. You could consider using an LLM to help with formatting and prettifying the information so that all the information is captured!

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
     git clone <repository-url>
     cd <repository-directory>
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

