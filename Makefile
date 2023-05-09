ARGS = $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

.Phony: test

test:
	python3 auto_bean_test.py

require:
	python3 -m pip install $(ARGS)

