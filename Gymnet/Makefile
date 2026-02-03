GymnetAdditionDir=$(PWD)/../Gymnet-addition

all: checkmakefiles
	cd src && $(MAKE)

clean: checkmakefiles
	cd src && $(MAKE) clean

cleanall: checkmakefiles
	cd src && $(MAKE) MODE=release clean
	cd src && $(MAKE) MODE=debug clean
	rm -f src/Makefile

# makefiles:
# 	cd src && opp_makemake -f --deep -I"$(GymnetAdditionDir)/include" -L"$(GymnetAdditionDir)/lib" -lzmq -lprotobuf -KEXTRA_OBJS="-Wl,--allow-multiple-definition"
# # 终于找到原因了，使用omnetpp5.6带的msys2中的clang版本编译protobuf 3.20.0有问题，遂降级为3.1版本；但后来又发现链接有问题，因为GymConnection中include了protobuf的h文件，而protobuf中的h文件有一些inline的函数定义，因此导致了一些符号重复（既在libprotobuf中存在又在GymConnection中存在），omnetpp6.1中的连接器可以自动忽视此错误，而omnetpp5.6中的连接器则会报error；经过检索，通过在LDFLAGS中添加“-Wl,--allow-multiple-definition”参数可以强制忽视此错误；然而opp_makemake不能直接传入此参数，故只能取巧通过EXTRA_OBJS传入此参数，问题解决！-chenyang,2026/2/3

# chenyang 2026/2/3, add support for Gymnet-NR
makefiles:
	@if [ "$(ENABLE_NR)" = "TRUE" ]; then \
	cd src && opp_makemake -f --deep -I"$(GymnetAdditionDir)/include" -I"$(GymnetAdditionDir)/gymnet-inet4/src" -I"$(GymnetAdditionDir)/gymnet-lte/src" -L"$(GymnetAdditionDir)/lib" -L"$(GymnetAdditionDir)/gymnet-inet4/src" -L"$(GymnetAdditionDir)/gymnet-lte/src" -lzmq -lprotobuf -lINET -lGYMNETLTE -KEXTRA_OBJS="-Wl,--allow-multiple-definition"; \
	else \
	cd src && opp_makemake -f --deep -I"$(GymnetAdditionDir)/include" -L"$(GymnetAdditionDir)/lib" -lzmq -lprotobuf -KEXTRA_OBJS="-Wl,--allow-multiple-definition";\
	fi

checkmakefiles:
	@if [ ! -f src/Makefile ]; then \
	echo; \
	echo '======================================================================='; \
	echo 'src/Makefile does not exist. Please use "make makefiles" to generate it!'; \
	echo '======================================================================='; \
	echo; \
	exit 1; \
	fi
