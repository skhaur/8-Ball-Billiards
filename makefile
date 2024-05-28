CC=clang
CFLAGS= -std=c99 -Wall -pedantic -fPIC
LIBS=-lm
PYTHON_PATH= -I/usr/include/python3.11
SWIG=swig

all: _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

libphylib.so: phylib.o  
	$(CC) -shared -o libphylib.so phylib.o $(LIBS)

phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c $(PYTHON_PATH) -fPIC -o phylib_wrap.o

_phylib.so: libphylib.so phylib_wrap.o
	$(CC) -shared phylib_wrap.o -L. $(PYTHON_PATH) -lphylib -lpython3.11 -o _phylib.so

clean:
	rm -f *.o *.so *.svg phylib_wrap.c phylib.py _phylib.so
