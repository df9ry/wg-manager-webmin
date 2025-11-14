# Makefile for WebMin WireGuard Manager
# Copyright (C) 2024 Reiner Hagn (df9ry)
# Copyright (C) 2024 DeepSeek AI

PACKAGE=webmin-wireguard-manager
VERSION=1.0
BUILDDIR=build

.PHONY: all build clean install deb test check-deps

all: build

check-deps:
	@echo "Checking build dependencies..."
	@for cmd in dpkg-buildpackage dh; do \
	 if ! command -v $$cmd >/dev/null 2>&1; then \
	  echo "❌ Missing: $$cmd - Install with: sudo apt install devscripts debhelper"; \
	  exit 1; \
	 fi; \
	done
	@echo "✅ All build dependencies available"

build: check-deps
	@echo "Building $(PACKAGE) version $(VERSION)"
	@mkdir -p $(BUILDDIR)
	@cp -r src scripts $(BUILDDIR)/
	@chmod +x $(BUILDDIR)/scripts/* $(BUILDDIR)/src/*.cgi

deb: check-deps
	@echo "Building Debian package..."
	dpkg-buildpackage -us -uc -b

clean:
	rm -rf $(BUILDDIR)
	rm -f ../$(PACKAGE)_*.deb
	dh_clean

install:
	@echo "Installing to /usr/share/webmin/wg-manager/"
	mkdir -p /usr/share/webmin/wg-manager
	cp -r src/* /usr/share/webmin/wg-manager/
	cp -r scripts/* /usr/share/webmin/wg-manager/
	chmod +x /usr/share/webmin/wg-manager/*.cgi
	chmod +x /usr/share/webmin/wg-manager/wg-*
	@echo "Installation complete. Refresh WebMin modules."

test:
	@echo "Running tests..."
	chmod +x tests/test_scripts.sh
	./tests/test_scripts.sh

dist:
	tar -czf $(PACKAGE)-$(VERSION).tar.gz \
	 --exclude=.git \
	 --exclude=build \
	 --exclude=*.deb \
	 .
	@echo "Source tarball created: $(PACKAGE)-$(VERSION).tar.gz"

help:
	@echo "Available targets:"
	@echo "  check-deps - Check build dependencies"
	@echo "  build      - Prepare build directory"
	@echo "  deb        - Build Debian package"
	@echo "  install    - Install directly to system"
	@echo "  test       - Run tests"
	@echo "  dist       - Create source tarball"
	@echo "  clean      - Clean build artifacts"