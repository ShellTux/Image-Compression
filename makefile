IMAGES := $(wildcard docs/*.png docs/*.jpg docs/*.jpeg docs/*.gif)

%.pdf: %.md $(IMAGES)
	pandoc --from=markdown-implicit_figures $< --output=$@
