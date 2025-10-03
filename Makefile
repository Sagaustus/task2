# Makefile — Grammar Checker (CMPUT 461/501)

# ---- Configurable paths ----
PY        ?= python3
DATA      ?= data/train.tsv
GRAMMAR   ?= grammars/toy.cfg
OUTPUT    ?= output/train.tsv
MET_JSON  ?= reports/metrics.json
MET_TXT   ?= reports/metrics.txt

# ---- Phony targets ----
.PHONY: help setup run eval show clean deepclean

help:
	@echo "Targets:"
	@echo "  make setup      - create venv and install dependencies"
	@echo "  make run        - run checker: $(DATA) + $(GRAMMAR) -> $(OUTPUT) and metrics"
	@echo "  make eval       - print metrics summary from $(MET_TXT)"
	@echo "  make show       - preview first 10 lines of $(OUTPUT)"
	@echo "  make clean      - remove generated outputs (keep venv)"
	@echo "  make deepclean  - clean everything including venv"
	@echo "  "
	@echo "Override defaults like: make run DATA=data/dev.tsv OUTPUT=output/dev.tsv"

# ---- Setup (virtualenv + deps) ----
.venv/bin/activate:
	$(PY) -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip
	. .venv/bin/activate; pip install nltk

setup: .venv/bin/activate
	@echo "Setup complete."

# ---- Run pipeline ----
run: setup
	. .venv/bin/activate; $(PY) src/main.py $(DATA) $(GRAMMAR) $(OUTPUT) \
	  --metrics_json $(MET_JSON) --metrics_txt $(MET_TXT)

# ---- Show metrics / output ----
eval:
	@echo "=== Metrics (from $(MET_TXT)) ==="; \
	if [ -f "$(MET_TXT)" ]; then cat "$(MET_TXT)"; else echo "No $(MET_TXT) found. Run 'make run' first."; fi

show:
	@echo "=== Preview: $(OUTPUT) ==="; \
	if [ -f "$(OUTPUT)" ]; then head -n 10 "$(OUTPUT)"; else echo "No $(OUTPUT) found. Run 'make run' first."; fi

# ---- Cleaning ----
clean:
	rm -f $(OUTPUT) $(MET_JSON) $(MET_TXT)
	@echo "Cleaned generated files."

deepclean: clean
	rm -rf .venv __pycache__ */__pycache__
	find . -name '*.pyc' -delete
	@echo "Deep cleaned (including venv)."
