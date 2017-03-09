LIBDIR=/apps/share64/debian7
ENVIRONDIR=${LIBDIR}/environ.d
ENVIRONPATH=${ENVIRONDIR}/gbsmaps-${REV}
GBSMAPSDIR=${LIBDIR}/gbsmaps
REV:=$(shell svn info | grep 'Revision: ' | awk '{ print $$2; }')
INSTALLDIR=${GBSMAPSDIR}/r${REV}
PYSITEDIR=${INSTALLDIR}/lib/python2.7/site-packages


all:
	python setup.py build

install:
	mkdir -p ${PYSITEDIR}
	PYTHONPATH=${PYSITEDIR}:${PYTHONPATH} python setup.py install --prefix ${INSTALLDIR}
	sed -e "s:REV:${REV}:" -e "s:INSTALLDIR:${INSTALLDIR}:" gbsmaps.use.in > ${ENVIRONPATH}
	chmod 644 ${ENVIRONPATH}

clean:
	python setup.py clean --all
	rm -rf dist GabbsMaps.egg-info

distclean: clean
	rm -rf ${INSTALLDIR}

.PHONY: all install clean distclean
