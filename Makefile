.PHONY: install run test
install:
	pip install -r requirements.txt
run:
	python -m pipeline.run
test:
	pytest -q
