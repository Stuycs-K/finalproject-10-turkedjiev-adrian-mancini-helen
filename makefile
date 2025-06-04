translate:
	@python3 translate.py $(ARGS)
run:
	@python3 translate.py $(ARGS) temp_script.py
	@python3 temp_script.py
	@rm temp_script.py