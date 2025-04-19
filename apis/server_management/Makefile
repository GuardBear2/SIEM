# Makefile for GuardBear API
# Copyright (C) 2015, GuardBear Inc.
# May 3, 2017
#
# Syntax: make [ all | backup | install | restore | service ]

GUARDBEAR_USER        = guardbear-server
GUARDBEAR_GROUP       = guardbear-server
GUARDBEAR_SERVER      = guardbear-server
SHARE_INSTALLDIR  ?= /usr/share/${GUARDBEAR_SERVER}
ETC_INSTALLDIR    ?= /etc/${GUARDBEAR_SERVER}
BIN_INSTALLDIR    ?= ${SHARE_INSTALLDIR}/bin


MV_FILE        = mv -f
RM_FILE        = rm -f
INSTALL_DIR    = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0750 -d
INSTALL_RW_DIR = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0770 -d
INSTALL_EXEC   = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0750
INSTALL_FILE   = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0640
INSTALL_CONFIG_FILE   = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0660
PYTHON_BIN     = $(SHARE_INSTALLDIR)/framework/python/bin/python3


.PHONY: install

install:
    # Copy files and create folders
	# SHARE
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/apis/scripts
	$(INSTALL_EXEC) scripts/guardbear_server_management_apid.py ${SHARE_INSTALLDIR}/apis/scripts/guardbear-server-management-apid.py

    # Install scripts/%.py on $(INSTALLDIR)/bin/%
	$(foreach script,$(wildcard scripts/*.py),$(INSTALL_EXEC) wrappers/generic_wrapper.sh $(patsubst scripts/%.py,${BIN_INSTALLDIR}/%,$(script));)

	$(MV_FILE) ${BIN_INSTALLDIR}/guardbear_server_management_apid ${BIN_INSTALLDIR}/guardbear-server-management-apid
