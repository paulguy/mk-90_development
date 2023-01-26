OBJECTS = test.obj
TARGET = test.bin
SMP = smp0.bin

all: macro11 $(SMP)

macro11:
	cd MACRO11/src && $(MAKE) -f makefile
	cp MACRO11/src/macro11 macro11

$(OBJECTS): %.obj: %.mac
	./macro11 -l /dev/stdout -yus -ysl 64 $? -o $@

$(TARGET): $(OBJECTS)
	./obj2bin.pl -rt11 --binary --nocrc --bytes=100000 --outfile=$@ $^

$(SMP): $(TARGET)
	dd if=$^ of=$@.tmp bs=1 skip=6
	# make it have at least 10KB
	dd if=$@.tmp of=$@ conv=sync bs=10240 count=1

.PHONY: clean distclean

clean:
	rm $(OBJECTS)
	rm $(TARGET)
	rm $(SMP)

distclean:
	cd MACRO11/src && $(MAKE) clean
	rm macro11
	rm $(OBJECTS)
	rm $(TARGET)
	rm $(SMP)
