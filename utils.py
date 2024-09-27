import json
import os


def load_articles_from_checkpoint(checkpoint_file="checkpoint.json", raw_articles_dir="raw_articles"):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
            articles = checkpoint_data['articles']
            
        if not os.path.exists(raw_articles_dir):
            os.makedirs(raw_articles_dir)
        
        for i, article in enumerate(articles):
            filename = os.path.join(raw_articles_dir, f"article_{i}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"URL: {article['url']}\n")
                f.write(f"Title: {article['title']}\n\n")
                f.write(article['content'])
        
        print(f"Loaded {len(articles)} articles from checkpoint and saved to {raw_articles_dir}")
    else:
        print("Checkpoint file not found.")


def load_articles_to_single_file(checkpoint_file="checkpoint.json", output_file="articles.txt"):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
            articles = checkpoint_data['articles']
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for article in articles:
                f.write(f"URL: {article['url']}\n")
                f.write(f"Title: {article['title']}\n\n")
                f.write(article['content'])
                f.write("\n\n" + "-"*50 + "\n\n")  # Separator between articles
        
        print(f"Loaded {len(articles)} articles from checkpoint and saved to {output_file}")
    else:
        print("Checkpoint file not found.")


if __name__ == "__main__":
    # checkpoint_file = "checkpoint.json"
    # raw_articles_dir = "raw_articles"
    # load_articles_from_checkpoint(checkpoint_file, raw_articles_dir)

    checkpoint_file = "checkpoint.json"
    output_file = "articles.txt"
    load_articles_to_single_file(checkpoint_file, output_file)
