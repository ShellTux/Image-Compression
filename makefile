%.pdf: %.md
	pandoc $< --output=$@
