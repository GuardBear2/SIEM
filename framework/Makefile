# Makefile for GuardBear Framework
# Copyright (C) 2015, GuardBear Inc.
# May 3, 2017
#
# Syntax: make [ all | build | install | examples | clean ]

GUARDBEAR_USER        = guardbear-server
GUARDBEAR_GROUP       = guardbear-server
GUARDBEAR_SERVER	  = guardbear-server

SHARE_INSTALLDIR       ?= /usr/share/${GUARDBEAR_SERVER}
LOG_INSTALLDIR         ?= /var/log/${GUARDBEAR_SERVER}
LIB_INSTALLDIR         ?= /var/lib/${GUARDBEAR_SERVER}
ETC_INSTALLDIR         ?= /etc/${GUARDBEAR_SERVER}
BIN_INSTALLDIR         ?= ${SHARE_INSTALLDIR}/bin

CC           = gcc
CFLAGS       = -pipe -Wall -Wextra
THREAD_FLAGS = -pthread
MV_FILE      = mv -f
RM_FILE      = rm -f
INSTALL_DIR  = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0750  -d
INSTALL_EXEC = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0750
INSTALL_FILE = install -o ${GUARDBEAR_USER} -g ${GUARDBEAR_GROUP} -m 0640

ifdef DEBUG
	CFLAGS+=-g -I ../src
	LFLAGS+=-g
else
	CFLAGS+=-O2 -I ../src
	LFLAGS+=-O2
endif

.PHONY: all build install examples clean

all: build

install:
	# SHARE
	$(INSTALL_DIR) $(BIN_INSTALLDIR)
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/scripts
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/guardbear
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/guardbear/core/cluster
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/guardbear/core/cluster/dapi
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/guardbear/core/cluster/hap_helper

	# LOGS
	$(INSTALL_DIR) $(LOG_INSTALLDIR)

	# ETC
	$(INSTALL_DIR) $(ETC_INSTALLDIR)
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/cluster
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/certs
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/groups

	# SHARE
	$(INSTALL_EXEC) scripts/guardbear_server.py ${SHARE_INSTALLDIR}/framework/scripts/guardbear-server.py
	$(INSTALL_FILE) guardbear/*.py ${SHARE_INSTALLDIR}/framework/guardbear
	$(INSTALL_FILE) guardbear/core/cluster/*.py ${SHARE_INSTALLDIR}/framework/guardbear/core/cluster
	$(INSTALL_FILE) guardbear/core/cluster/dapi/*.py ${SHARE_INSTALLDIR}/framework/guardbear/core/cluster/dapi
	$(INSTALL_FILE) guardbear/core/cluster/hap_helper/*.py ${SHARE_INSTALLDIR}/framework/guardbear/core/cluster/hap_helper

	# ETC
	$(INSTALL_FILE) ../etc/guardbear-server.yml ${ETC_INSTALLDIR}


	# BIN
#	Install scripts/%.py on $(INSTALLDIR)/bin/%
	$(foreach script,$(wildcard scripts/*.py),$(INSTALL_EXEC) wrappers/generic_wrapper.sh $(patsubst scripts/%.py,${BIN_INSTALLDIR}/%,$(script));)
#   Provisional name change for guardbear-logtest and guardbear-clusterd
	$(MV_FILE) ${BIN_INSTALLDIR}/guardbear_server ${BIN_INSTALLDIR}/guardbear-server
	$(RM_FILE) ${BIN_INSTALLDIR}/__init__

examples: install
	$(INSTALL_DIR) $(INSTALLDIR)/framework/examples
	$(INSTALL_EXEC) examples/*.py ${INSTALLDIR}/framework/examples

clean:
	$(RM_FILE) $(BUILD_TARGET) *.o *.so.0
