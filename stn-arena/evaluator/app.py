"""⟨STN-ARENA⟩ private evaluator — runs INSIDE the private Space.

Reads:   submissions dataset (public)
Scores:  against the PRIVATE battery + answer key (mounted as a private file,
         never published): /private/answers.json + /private/generator.py
Writes:  results dataset (public)

The battery, the answer key and the manuscript generator NEVER leave this
Space. Scores are reproducible: the run manifest (seed, battery version,
weight vector) is published with every results batch.

© 2026 Luka Pintarič, VBL 0.1210 (§0.9, §0.10, §0.12) — executor: Mera (AI).
"""
import json
import os
import datetime
import gradio as gr
from huggingface_hub import hf_hub_download, HfApi
import scoring

SUBMISSIONS = os.environ.get("DATASET_SUBMISSIONS", "AtmaOVictu/stn-arena-submissions")
RESULTS = os.environ.get("DATASET_RESULTS", "AtmaOVictu/stn-arena-results")
TOKEN = os.environ.get("HF_TOKEN")
api = HfApi(token=TOKEN)


def load_submissions():
    path = hf_hub_download(SUBMISSIONS, "submissions.jsonl", repo_type="dataset")
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def score_one(sub, answers):
    t = sub["transcript"]
    m = {
        "Hi": scoring.score_hi(t, answers),
        "Zi": scoring.score_zi(t, answers),
        "K": scoring.score_k(t, answers),
        "Ri": scoring.score_ri(t, answers),
        "Ck": scoring.score_ck(t, answers),
        "V": scoring.score_v(t, answers),
    }
    m["overall"] = scoring.overall(**m)
    m.update({k: sub[k] for k in
              ("model_name", "submitted_by", "submission_time", "seed")})
    return m


def run():
    with open("/private/answers.json", encoding="utf-8") as f:
        answers = json.load(f)  # private battery + answer key
    results = [score_one(s, answers) for s in load_submissions()]
    payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results)
    api.upload_file(path_or_fileobj=payload.encode("utf-8"),
                    path_in_repo="results.jsonl", repo_id=RESULTS,
                    repo_type="dataset")
    return f"scored {len(results)} submissions"


with gr.Blocks() as demo:
    status = gr.Textbox(label="status")
    btn = gr.Button("score pending submissions")
    btn.click(lambda: run(), outputs=status)

demo.launch()
