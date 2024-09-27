from dotenv import load_dotenv
import json
import os

from chunking_evaluation import SyntheticEvaluation
from chunking_evaluation import BaseChunker
from chunking_evaluation.chunking import RecursiveTokenChunker, ClusterSemanticChunker, KamradtModifiedChunker, LLMSemanticChunker

from chunker import LLMChunker

load_dotenv()

# Specify the corpora paths and output CSV file

raw_articles_dir = "raw_articles"
corpora_paths = [
    os.path.join(raw_articles_dir, f"article_{i}.txt")
    for i in range(50)
    if os.path.exists(os.path.join(raw_articles_dir, f"article_{i}.txt"))
]

queries_csv_path = 'generated_queries_excerpts.csv'

# Initialize the evaluation
evaluation = SyntheticEvaluation(corpora_paths, queries_csv_path, openai_api_key=os.getenv("OPENAI_API_KEY"))


# Generate queries and excerpts, and save to CSV
evaluation.generate_queries_and_excerpts(num_rounds=1, queries_per_corpus=2)
evaluation.filter_poor_excerpts(threshold=0.36)
evaluation.filter_duplicates(threshold=0.6)

# Define a custom chunking class
class NaiveChunker(BaseChunker):
    def split_text(self, text):
        # Custom chunking logic
        return [text[i:i+750] for i in range(0, len(text), 750)]

# Function to run evaluation on multiple chunkers and save results
def run_and_save_evaluations(evaluation):
    chunkers = [
        RecursiveTokenChunker(),
        ClusterSemanticChunker(),
        KamradtModifiedChunker(),
        NaiveChunker(),
        LLMSemanticChunker(),
    ]
    
    results = {}
    for chunker in chunkers:
        chunker_name = chunker.__class__.__name__
        print(f"Running evaluation for {chunker_name}...")
        results[chunker_name] = evaluation.run(chunker)
    
    # Save results to a file
    with open('chunker_evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Evaluation results saved to chunker_evaluation_results.json")
    return results


if __name__ == "__main__":
    # Run evaluations and save results
    evaluation_results = run_and_save_evaluations(evaluation)
    
    # Print summary of results
    def report_metrics_from_json(json_file='chunker_evaluation_results.json'):
        with open(json_file, 'r') as f:
            results = json.load(f)
        
        print("\nEvaluation Results Summary:")
        for chunker_name, chunker_results in results.items():
            precision_mean = chunker_results['precision_mean']
            recall_mean = chunker_results['recall_mean']
            iou_mean = chunker_results['iou_mean']
            
            print(f"{chunker_name}:")
            print(f"  Precision Mean: {precision_mean:.4f}")
            print(f"  Recall Mean: {recall_mean:.4f}")
            print(f"  IOU Mean: {iou_mean:.4f}")
            print()

    # Call the function to report metrics
    report_metrics_from_json()
