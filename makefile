tei = les-temps-de-la-fin.tei
schema_name = tei-ud

.PHONY: validate

validate:
	jing -c $(schema_name).rnc $(tei)
	xmlstarlet validate --err --dtd $(schema_name).dtd $(tei)
