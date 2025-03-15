ARCHIVE        = Multimedia-PL2-G1.zip
IMAGES         = $(shell grep --only-matching 'docs/.*\.png' docs/relatorio.md)
PYTHON_SCRIPTS = $(shell find src -type f -name "step*.py" | sort --unique | grep --invert-match 'test')
REPORT         = docs/relatorio.pdf

PANDOC_OPTS += --resource-path=docs
PANDOC_OPTS += --filter=pandoc-include

%.pdf: %.md $(PYTHON_SCRIPTS)
	./generate-images.sh
	pandoc $(PANDOC_OPTS) --output=$@ $<

$(ARCHIVE): $(REPORT) $(IMAGES)
	git archive --verbose --format=zip $(^:%=--add-file=% ) --output=$@ HEAD

.PHONY: archive
archive: $(ARCHIVE)
