PYTHON ?= python3
DEMO_OUT ?= $(shell $(PYTHON) -c "import os,tempfile;print(os.path.join(tempfile.gettempdir(),'telegraph-evaluation-opportunities-demo.json'))")

.PHONY: help test docs validate prepush bootstrap project seed-h2 launch-check launch-check-live evaluation-demo

help:
	@echo "make test         - run all JS and Python tests"
	@echo "make docs         - regenerate human-readable catalogue docs"
	@echo "make validate     - validate catalogue / seed data"
	@echo "make prepush      - full structural check before git push"
	@echo "make bootstrap    - configure labels/topics/settings on current GitHub repo"
	@echo "make project      - create optional maintainer GitHub Project"
	@echo "make seed-h2      - publish approved H2 seed Issues (publish=true only)"
	@echo "make launch-check - initial offline H2 seed announcement data gate"
	@echo "make launch-check-live - check actual live GitHub Issues (ongoing/H2; requires gh auth)"
	@echo "make evaluation-demo - safe offline example of Category/Intent gap grouping"

test:
	npm test

docs:
	$(PYTHON) scripts/generate_docs.py

validate:
	$(PYTHON) scripts/validate_catalog.py

prepush: validate
	$(PYTHON) scripts/generate_docs.py --check
	$(PYTHON) scripts/prepush.py

bootstrap: prepush
	bash scripts/bootstrap_github.sh

project:
	bash scripts/create_project.sh

seed-h2: validate
	$(PYTHON) scripts/seed_h2_issues.py

launch-check: prepush
	$(PYTHON) scripts/launch_check.py

launch-check-live: prepush
	$(PYTHON) scripts/launch_check.py --live

evaluation-demo:
	@TELEGRAPH_BOUNTY_PUBLICATION_KEY=$$($(PYTHON) -c 'import secrets; print(secrets.token_urlsafe(32))') $(PYTHON) scripts/evaluation_opportunities.py --profiles examples/evaluation-profiles.example.json --snapshot examples/evaluation-state.example.ndjson --now 2026-10-11T10:00:00Z --output "$(DEMO_OUT)"
	./tb needs "$(DEMO_OUT)"
