UV := .tools/bin/uv
export UV_CACHE_DIR := $(CURDIR)/.uv-cache

.PHONY: sync test
sync:
	$(UV) sync --locked

test:
	$(UV) run --locked pytest
