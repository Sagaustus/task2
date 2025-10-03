# Grammar Checker – Results & Justifications

**Course:** CMPUT 461/501 — Intro to NLP  
**Assignment:** A2 – Grammar Checker  

## 1) Final Results

- **Precision:** 0.2275  
- **Recall:** 0.7986  

**Confusion Matrix (prediction: 1 = “has grammar errors”, 0 = “no errors”):**

|             | ground_truth = 1 | ground_truth = 0 |
|-------------|------------------|------------------|
| prediction = 1 | TP = 111        | FP = 377        |
| prediction = 0 | FN = 28        | TN = 87        |

*Notes.* We follow the assignment’s convention and equations for precision and recall.  

## 2) Error Analysis

**Where false positives (FP) likely came from (up to 3):**
1. Missing sentence-initial adverbial or subordinate-clause structures, causing otherwise grammatical openings to fail.
2. Limited handling of stacked auxiliaries or modals followed by negation, leading to parse failure despite valid syntax.
3. Sparse coordination patterns, especially for adjectives or verb phrases with trailing punctuation variations.

**Where false negatives (FN) likely came from (up to 3):**
1. NP and VP recursion rules (e.g., NP → NP PP, VP → VP PP) over-generate sequences that should be flagged as errors.
2. Lack of agreement constraints lets mismatched number or tense combinations parse successfully.
3. Generic verb and noun preterminals accept malformed tag orders such as repeated verbs without auxiliaries.

**Suggested improvements (brief):**  
- Add targeted clause-level rules (e.g., SBAR complements, sentence-initial adverbs) and richer coordination coverage.  
- Incorporate lightweight agreement checks or feature annotations to block obvious mismatches.  
- Add post-parse heuristics or penalty scoring to down-rank over-generated structures.

## 3) Iteration Count

I iterated roughly **4** times in the modify–evaluate loop (small grammar tweaks + re-run on the dataset).

## 4) Is a Perfect Checker Possible with this Design?

A perfect checker is unlikely with the current CFG-only design because pure POS-level rules cannot capture the full variety of English syntax, semantics, or agreement phenomena needed for flawless judgments.

Achieving near-perfect coverage would require a much richer rule set, feature-based agreement, and potentially statistical scoring or machine-learning components—resources beyond the scope of this lightweight rule-based prototype.

## 5) Reproducibility

- **Grammar:** `grammars/toy.cfg`  
- **Runner:** `python3 src/main.py data/train.tsv grammars/toy.cfg output/train.tsv`  
- **Metrics saved to:** `reports/metrics.json`, `reports/metrics.txt`  

