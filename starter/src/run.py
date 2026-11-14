"""Main pipeline runner: chunking, embedding, vector store upsert, and benchmark evaluation."""
import json
import time
import os
import csv
from pathlib import Path

from .models import Chunk, DocumentPage
from .ingestion import load_pdf
from .chunking import fixed_size, by_paragraph
from .embeddings import MyEmbedder
from .store import ChromaVectorStore
from .evaluation import evaluate_query, summarize


def run_pipeline() -> dict:
    start_time = time.time()
    print("=" * 60)
    print("STARTING DAY 06 DATA INGESTION & BENCHMARK PIPELINE")
    print("=" * 60)

    # 1. Load Corpus
    pdf_path = Path("starter/data/Quy-che-3626-digital.pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(f"Corpus PDF not found at {pdf_path}")
    
    pages = load_pdf(pdf_path, document_id="vnu_uet_quy_che_3626", source="Quy-che-3626-digital.pdf")
    print(f"[1] Loaded {len(pages)} content pages from {pdf_path.name}")
    if len(pages) < 30:
        raise ValueError(f"Requirement failed: Expected >= 30 pages, got {len(pages)}")

    # 2. Load Benchmark
    benchmark_path = Path("benchmark/benchmark.json")
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark not found at {benchmark_path}")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)
    print(f"[2] Loaded {len(benchmark)} benchmark questions (Dev: {sum(1 for q in benchmark if q['split']=='dev')}, Test: {sum(1 for q in benchmark if q['split']=='test')})")

    # 3. Build Chunks
    print("\n[3] Generating chunks for Strategies A, B, and C...")
    # Strategy A: Fixed size 500, overlap 50
    chunks_A: list[Chunk] = []
    for p in pages:
        chunks_A.extend(fixed_size(p, size=500, overlap=50))
    print(f" -> Strategy A (Fixed size 500/50): {len(chunks_A)} chunks")

    # Strategy B & C: By paragraph/structure (max 800)
    chunks_B: list[Chunk] = []
    for p in pages:
        chunks_B.extend(by_paragraph(p, max_size=800))
    print(f" -> Strategy B & C (Paragraph max 800): {len(chunks_B)} chunks")

    # 4. Initialize Embedder & Vector Store
    print("\n[4] Initializing Embedder & Vector Store...")
    embedder = MyEmbedder(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    print(f" -> Model: {embedder.model_name} (Dimensions: {embedder.dimensions})")

    vector_store = ChromaVectorStore(persist_dir="starter/data/chroma_db", dimensions=embedder.dimensions)
    vector_store.create_schema()

    # Ingest Strategy A
    t_a0 = time.time()
    texts_A = [c.text for c in chunks_A]
    print(f" -> Embedding Strategy A ({len(texts_A)} chunks)...")
    vectors_A = embedder.embed_documents(texts_A)
    vector_store.upsert("A", chunks_A, vectors_A)
    t_ingest_A = round(time.time() - t_a0, 2)
    print(f" -> Strategy A ingested in {t_ingest_A}s")

    # Ingest Strategy B & C
    t_b0 = time.time()
    texts_B = [c.text for c in chunks_B]
    print(f" -> Embedding Strategy B & C ({len(texts_B)} chunks)...")
    vectors_B = embedder.embed_documents(texts_B)
    vector_store.upsert("B", chunks_B, vectors_B)
    vector_store.upsert("C", chunks_B, vectors_B)
    t_ingest_B = round(time.time() - t_b0, 2)
    t_ingest_C = t_ingest_B
    print(f" -> Strategy B & C ingested in {t_ingest_B}s")

    # 5. Run Benchmark Queries
    print("\n[5] Running Benchmark Evaluation on Dev & Test splits...")
    os.makedirs("results", exist_ok=True)
    traces = {"A": [], "B": [], "C": []}

    for strat in ["A", "B", "C"]:
        print(f" -> Evaluating Strategy {strat}...")
        for q in benchmark:
            q_emb = embedder.embed_query(q["question"])
            
            # For Strategy C: apply metadata filter if available in question
            flt = q.get("filter") if strat == "C" else None
            
            hits = vector_store.search(
                strategy=strat,
                query_vector=q_emb,
                top_k=3,
                filters=flt
            )
            
            trace_item = evaluate_query(q, hits)
            traces[strat].append(trace_item)

        # Save strategy trace
        trace_file = Path(f"results/trace_strategy_{strat}.json")
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(traces[strat], f, ensure_ascii=False, indent=2)
        print(f"    Saved trace to {trace_file}")

    # 6. Compute Summaries
    print("\n[6] Computing Metric Summaries...")
    summary_results = {}
    for strat in ["A", "B", "C"]:
        summary_results[strat] = summarize(traces[strat])
        summary_results[strat]["chunk_count"] = len(chunks_A) if strat == "A" else len(chunks_B)
        summary_results[strat]["ingest_time_seconds"] = t_ingest_A if strat == "A" else t_ingest_B
        summary_results[strat]["cost_usd"] = 0.0

    summary_file = Path("results/summary_metrics.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_results, f, ensure_ascii=False, indent=2)
    print(f"Saved summary to {summary_file}")

    # 7. Update artifacts/experiment_log.csv
    log_csv_path = Path("artifacts/experiment_log.csv")
    with open(log_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "strategy", "chunking", "chunk_size", "overlap", "metadata", "filter",
            "vectorizer", "hypothesis", "dev_hit1", "dev_hit3", "test_hit1", "test_hit3", "notes"
        ])
        
        # A
        writer.writerow([
            "A", "fixed", 500, 50, "source,page,chapter", "none",
            "paraphrase-multilingual-MiniLM-L12-v2",
            "Fixed-size chunking baseline",
            f"{summary_results['A']['dev']['hit1_count']}/{summary_results['A']['dev']['total']}",
            f"{summary_results['A']['dev']['hit3_count']}/{summary_results['A']['dev']['total']}",
            f"{summary_results['A']['test']['hit1_count']}/{summary_results['A']['test']['total']}",
            f"{summary_results['A']['test']['hit3_count']}/{summary_results['A']['test']['total']}",
            f"Ingest {t_ingest_A}s, {len(chunks_A)} chunks"
        ])
        # B
        writer.writerow([
            "B", "paragraph", 800, 0, "source,page,chapter", "none",
            "paraphrase-multilingual-MiniLM-L12-v2",
            "Structure-aware chunking preserves coherence",
            f"{summary_results['B']['dev']['hit1_count']}/{summary_results['B']['dev']['total']}",
            f"{summary_results['B']['dev']['hit3_count']}/{summary_results['B']['dev']['total']}",
            f"{summary_results['B']['test']['hit1_count']}/{summary_results['B']['test']['total']}",
            f"{summary_results['B']['test']['hit3_count']}/{summary_results['B']['test']['total']}",
            f"Ingest {t_ingest_B}s, {len(chunks_B)} chunks"
        ])
        # C
        writer.writerow([
            "C", "paragraph", 800, 0, "source,page,chapter", "chapter filter",
            "paraphrase-multilingual-MiniLM-L12-v2",
            "Metadata filtering narrows scope and eliminates out-of-chapter distractors",
            f"{summary_results['C']['dev']['hit1_count']}/{summary_results['C']['dev']['total']}",
            f"{summary_results['C']['dev']['hit3_count']}/{summary_results['C']['dev']['total']}",
            f"{summary_results['C']['test']['hit1_count']}/{summary_results['C']['test']['total']}",
            f"{summary_results['C']['test']['hit3_count']}/{summary_results['C']['test']['total']}",
            f"Ingest {t_ingest_C}s, {len(chunks_B)} chunks"
        ])
    print(f"Updated {log_csv_path}")

    # 8. Print formatted report table
    print("\n" + "=" * 70)
    print("BENCHMARK RETRIEVAL ACCURACY REPORT")
    print("=" * 70)
    print(f"{'Strategy':<10} | {'Split':<6} | {'Hit@1 (n/N)':<12} | {'Hit@3 (n/N)':<12} | {'Chunks':<8} | {'Time (s)':<8}")
    print("-" * 70)
    for strat in ["A", "B", "C"]:
        dev_res = summary_results[strat]["dev"]
        test_res = summary_results[strat]["test"]
        c_cnt = summary_results[strat]["chunk_count"]
        t_ing = summary_results[strat]["ingest_time_seconds"]
        
        print(f"{strat:<10} | {'dev':<6} | {dev_res['hit1_count']}/{dev_res['total']:<10} | {dev_res['hit3_count']}/{dev_res['total']:<10} | {c_cnt:<8} | {t_ing:<8}")
        print(f"{strat:<10} | {'test':<6} | {test_res['hit1_count']}/{test_res['total']:<10} | {test_res['hit3_count']}/{test_res['total']:<10} | {c_cnt:<8} | {t_ing:<8}")
        print("-" * 70)

    total_time = round(time.time() - start_time, 2)
    print(f"Pipeline completed successfully in {total_time}s!")
    return summary_results


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
