name = les-temps-de-la-fin
tei = $(name).tei
no-ud = $(name)-no-ud.tei
html = $(name).html

schema_name = tei-ud
dtd = $(schema_name).dtd
odd = $(schema_name).odd
rnc = $(schema_name).rnc

py = venv/bin/python3
pip = venv/bin/pip3

.PHONY: all validate clean

# $(html): tohtml.py $(tei) style.css
# 	make venv
# 	$(py) $^ $@

$(html): tohtml.xsl $(tei)
	xmlstarlet tr $^ > $@

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
$(ud_to_msd):

clean:
	rm -rf __pycache__ $(no-ud) $(html)
