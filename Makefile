init:
	pip install -r requirements.txt

test:
	python3 -m unittest discover

.PHONY: init test