ARCHIVE  = Multimedia-PL2-G1.zip
IMAGES  := $(wildcard docs/*.png docs/*.jpg docs/*.jpeg docs/*.gif)
REPORT   = docs/relatorio.pdf

PANDOC_OPTS += --resource-path=docs
PANDOC_OPTS += --filter=pandoc-include

$(ARCHIVE): $(REPORT)
	git archive --verbose --format=zip $(^:%=--add-file=% ) --output=$@ HEAD

%.pdf: %.md $(IMAGES)
	pandoc $(PANDOC_OPTS) --output=$@ $<
