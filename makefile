tei = les-temps-de-la-fin.tei

schema_name = tei-ud
dtd = $(schema_name).dtd
odd = $(schema_name).odd
rnc = $(schema_name).rnc

venv = venv
py = $(venv)/bin/python3
pip = $(venv)/bin/pip3


.PHONY: validate

validate:
	jing -c $(rnc) $(tei)
	xmlstarlet validate --err --dtd $(dtd) $(tei)

les-temps-de-la-fin-no-ud.tei: $(tei)
	$(py) ud_to_msd.py $< $@

$(venv):
	python3 -m venv $(venv)
	$(pip) install -r requirements.txt

clean:
	rm -rf __pycache__
