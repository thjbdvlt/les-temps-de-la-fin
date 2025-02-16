name = les-temps-de-la-fin
tei = $(name).tei
no-ud = $(name)-no-ud.tei
html = $(name).html tenses/cnd.html tenses/fut.html tenses/past.html tenses/pres.html tenses/imp.html

schema_name = tei-ud
dtd = $(schema_name).dtd
odd = $(schema_name).odd
rnc = $(schema_name).rnc
css = style.css

py = venv/bin/python3
pip = venv/bin/pip3

.PHONY: all validate clean to_msd navigate

all: to_msd validate

validate:
	jing -c $(rnc) $(tei)
	xmlstarlet validate --err --dtd $(dtd) $(tei)

$(html): to_html.py $(tei)
	mkdir -p tenses
	$(py) $^ $(css) $@

navigate: $(html)
	$(BROWSER) $<

to_msd: $(no-ud)

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
