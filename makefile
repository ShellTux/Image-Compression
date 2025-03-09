ARCHIVE        = Multimedia-PL2-G1.zip
IMAGES         = $(shell grep --only-matching 'docs/[0-9a-zA-Z-]\+.png' docs/relatorio.md)
PYTHON_SCRIPTS = $(shell find src -type f -name "step*.py" | sort --unique | grep --invert-match 'test')
REPORT         = docs/relatorio.pdf

PANDOC_OPTS += --resource-path=docs
PANDOC_OPTS += --filter=pandoc-include

$(ARCHIVE): $(REPORT)
	git archive --verbose --format=zip $(^:%=--add-file=% ) --output=$@ HEAD

%.pdf: %.md $(IMAGES)
	pandoc $(PANDOC_OPTS) --output=$@ $<
