tei = les-temps-de-la-fin.tei
no-ud = les-temps-de-la-fin-no-ud.tei

schema_name = tei-ud
dtd = $(schema_name).dtd
odd = $(schema_name).odd
rnc = $(schema_name).rnc

py = venv/bin/python3
pip = venv/bin/pip3


.PHONY: all validate clean

all: clean $(no-ud) validate

validate:
	jing -c $(rnc) $(tei)
	xmlstarlet validate --err --dtd $(dtd) $(tei)

$(no-ud): ud_to_msd.py $(tei)
	make venv
	$(py) $^ $@

venv:
	python3 -m venv venv
	$(pip) install -r requirements.txt

$(tei):

clean:
	rm -rf __pycache__ $(no-ud)
