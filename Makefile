ARGS = $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

.Phony: test

test:
	python3.11 auto_bean_test.py

require:
	python3.11 -m pip install $(ARGS)

run:
	python3.11 cli.py ./ignore/2023.bean