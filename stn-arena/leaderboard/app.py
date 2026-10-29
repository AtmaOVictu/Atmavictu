"""⟨STN-ARENA⟩ public leaderboard — Gradio Space.

Reads:   results dataset     (env DATASET_RESULTS)
Writes:  submissions dataset (env DATASET_SUBMISSIONS)
Private: nothing. The answer key lives only in the evaluator Space.

© 2026 Luka Pintarič, VBL 0.1210 (§0.9, §0.10, §0.12) — executor: Mera (AI).
"""
import json
import os
import datetime
import gradio as gr
from datasets import load_dataset
from huggingface_hub import HfApi, hf_hub_download

RESULTS = os.environ.get("DATASET_RESULTS", "AtmaOVictu/stn-arena-results")
SUBMISSIONS = os.environ.get("DATASET_SUBMISSIONS", "AtmaOVictu/stn-arena-submissions")
TOKEN = os.environ.get("HF_TOKEN")
api = HfApi(token=TOKEN)

HEADER = ["model", "submitted_by", "seed", "Hi", "Zi", "K", "Ri", "Ck", "V", "overall"]


def render_table():
    try:
        ds = load_dataset(RESULTS, split="train")
        rows = sorted(ds, key=lambda r: -float(r.get("overall") or 0))
        return [[r.get("model_name", ""), r.get("submitted_by", ""), r.get("seed", ""),
                 r.get("Hi"), r.get("Zi"), r.get("K"), r.get("Ri"), r.get("Ck"),
                 r.get("V"), r.get("overall")] for r in rows]
    except Exception as e:
        return [["(no results yet)", str(e)[:60], "", "", "", "", "", "", "", ""]]


def submit(model_name, submitted_by, seed, transcript_json):
    try:
        record = json.loads(transcript_json)
    except json.JSONDecodeError as e:
        return f"REJECTED — transcript is not valid JSON: {e}"
    record["model_name"] = model_name
    record["submitted_by"] = submitted_by
    record["seed"] = int(seed)
    record["submission_time"] = datetime.datetime.now(
        datetime.timezone.utc).isoformat(timespec="seconds")
    line = json.dumps(record, ensure_ascii=False) + "\n"
    try:
        path = hf_hub_download(SUBMISSIONS, "submissions.jsonl", repo_type="dataset")
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
        api.upload_file(path_or_fileobj=path.encode("utf-8"),
                        path_in_repo="submissions.jsonl", repo_id=SUBMISSIONS,
                        repo_type="dataset")
    except Exception:
        api.upload_file(path_or_fileobj=line.encode("utf-8"),
                        path_in_repo="submissions.jsonl", repo_id=SUBMISSIONS,
                        repo_type="dataset")
    return ("ACCEPTED — queued for scoring. Raw transcripts only; post-edited
            "submissions are void.")


with gr.Blocks(title="STN Arena") as demo:
    gr.Markdown("⟨STN-ARENA⟩ — Graded Test of Model Ignorance. Public leaderboard,
                " private ground truth. Nobody — including the operator — can fake a result.")
    gr.Dataframe(value=render_table, headers=HEADER, every=300, label="Leaderboard")
    with gr.Accordion("Submit a model"):
        m = gr.Textbox(label="model_name")
        s = gr.Textbox(label="submitted_by")
        sd = gr.Number(label="seed (from current run manifest)", precision=0)
        t = gr.Code(label="transcript JSON (schemas/submission.schema.json)", language="json")
        out = gr.Textbox(label="result")
        btn = gr.Button("submit")
        btn.click(submit, inputs=[m, s, sd, t], outputs=out)

demo.launch()
