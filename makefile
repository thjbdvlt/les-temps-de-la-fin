tei = les-temps-de-la-fin.tei
odd = schema.odd
rnc = schema.rnc

.PHONY: validate

validate:
	jing -c $(rnc) $(tei)
