###############
# Usage
###############
# Makefile to quickly build and run test files.
# Use:
# 	make - run all tests
#	make clean - delete built tests and test output
################

############
# Constants
###########
# the dist
REPYTAR=seattle_linux.tgz
# the untared dir
REPYDIR=seattle_repy
REPYPP=${REPYDIR}/repypp.py

# test
TESTDIR=tmp_test_dir
BUILDDIR=tmp_build_dir

SRCS=sockettimeout.repy
FN=z_test_*
RESTR_FN=restrictions.default

#############
# Public Commands
#############

all: build test

clean: 
	# test 
	rm -rf ${TESTDIR} ${BUILDDIR}

################
# Private Commands
###############

# Run seattle's test script.  Test should be built first.
test: 
	cd ${TESTDIR} && python run_tests.py

# Builds all test files
# Takes FN as arg, ex. `make FN=*controller*` to build all files with glob.
build: repy
	if [ ! -e ${BUILDDIR} ]; then mkdir ${BUILDDIR}; cp build.sh ${BUILDDIR}; fi
	cp ../../${SRCS} ${BUILDDIR}
	cp *${FN}* ${BUILDDIR}

	# create and populate the test dir
	cd ${BUILDDIR} && ./build.sh ${TESTDIR} "*${FN}*"

	cp restrictions.* ${TESTDIR}
	cp run_tests.py ${TESTDIR}	
	cp ${REPYDIR}/*.py ${TESTDIR}

superclean: clean
	rm -rf ${REPYDIR}

# download repy
repy:   
	# Dowloading Repy...
	if [ ! -e ${REPYDIR} ]; then wget --no-check-certificate https://seattlegeni.cs.washington.edu/geni/download/flibble/${REPYTAR}; tar xzf ${REPYTAR}; rm -f ${REPYTAR}; fi
	# done.
	#
