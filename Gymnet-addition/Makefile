zmq_dir=$(PWD)/zeromq-4.3.5
protobuf_dir=$(PWD)/protobuf-3.1.0
GymnetINET_dir=$(PWD)/gymnet-inet4
GymnetLTE_dir=$(PWD)/gymnet-lte

.PHONY: all cleanall zmq clean-zmq protobuf clean-protobuf gymnet-inet4 clean-gymnet-inet4 gymnet-lte clean-gymnet-lte

all: zmq protobuf gymnet-inet4 gymnet-lte

cleanall: clean-zmq clean-protobuf clean-gymnet-inet4 clean-gymnet-lte

zmq:
	cd $(zmq_dir) && ./configure --prefix=$(PWD) CXXFLAGS="-std=c++17 -Wno-format"
	cd $(zmq_dir) && make all $(MAKEFLAGS)
	cd $(zmq_dir) && make install

clean-zmq:
	cd $(zmq_dir) && make uninstall
	cd $(zmq_dir) && make distclean

protobuf:
	cd $(protobuf_dir) && ./configure --prefix=$(PWD) CXXFLAGS="-std=c++17 -Wno-format"
	cd $(protobuf_dir) && make all $(MAKEFLAGS)
	cd $(protobuf_dir) && make install

clean-protobuf:
	cd $(protobuf_dir) && make uninstall
	cd $(protobuf_dir) && make distclean


INET_SETENV = INET_ROOT=$(GymnetINET_dir) PATH=$(GymnetINET_dir)/bin:$(PATH) INET_NED_PATH=$(GymnetINET_dir)/src INET_OMNETPP_OPTIONS="-n $(GymnetINET_dir)/src" INET_GDB_OPTIONS="-quiet -ex run --args" INET_VALGRIND_OPTIONS="-v --tool=memcheck --leak-check=yes --show-reachable=no --leak-resolution=high --num-callers=40 --freelist-vol=4000000"
gymnet-inet4:
	cd gymnet-inet4 && $(INET_SETENV) make makefiles
	cd gymnet-inet4 && $(INET_SETENV) make all $(MAKEFLAGS)
	cp gymnet-inet4/src/libINET* ./bin

clean-gymnet-inet4:
	cd gymnet-inet4 && make cleanall
	rm -f ./bin/libINET*

gymnet-lte:
	cd $(GymnetLTE_dir) && INET_ROOT=$(GymnetINET_dir) make makefiles
	cd $(GymnetLTE_dir) && INET_ROOT=$(GymnetINET_dir) make all $(MAKEFLAGS)
	cp $(GymnetLTE_dir)/src/libGYMNETLTE* ./bin

clean-gymnet-lte:
	cd $(GymnetLTE_dir) && make cleanall
	rm -f ./bin/libGYMNETLTE*