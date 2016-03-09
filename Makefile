# This is to speed up development time.
# Usage:
#     Needed once:
#         $ virtualenv venv
#         $ . venv/bin/activate
#         $ pip install -e .`
#         $ pip install werkzeug
#     Once that is done, to rebuild simply:
#         $ make -j 4 && python -m unittest sasstests

PY_HEADERS := -I/usr/include/python2.7
C_SOURCES := $(wildcard libsass/src/*.c)
C_OBJECTS = $(patsubst libsass/src/%.c,build2/libsass/c/%.o,$(C_SOURCES))
CPP_SOURCES := $(wildcard libsass/src/*.cpp)
CPP_OBJECTS = $(patsubst libsass/src/%.cpp,build2/libsass/cpp/%.o,$(CPP_SOURCES))

all: _sass.so

build2/libsass/c/%.o: libsass/src/%.c
	@mkdir -p build2/libsass/c/
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I./libsass/include $(PY_HEADERS) -c $^ -o $@ -c -O2 -fPIC -std=c++0x -Wall -Wno-parentheses -Werror=switch

build2/libsass/cpp/%.o: libsass/src/%.cpp
	@mkdir -p build2/libsass/cpp/
	gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I./libsass/include $(PY_HEADERS) -c $^ -o $@ -c -O2 -fPIC -std=c++0x -Wall -Wno-parentheses -Werror=switch

build2/pysass.o: pysass.cpp
	@mkdir -p build2
	gcc -pthread -fno-strict-aliasing -Wno-write-strings -DNDEBUG -g -fwrapv -O2 -Wall -fPIC -I./libsass/include $(PY_HEADERS) -c $^ -o $@ -c -O2 -fPIC -std=c++0x -Wall -Wno-parentheses -Werror=switch

_sass.so: $(C_OBJECTS) $(CPP_OBJECTS) build2/pysass.o
	g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro $^ -L./libsass -o $@ -fPIC -lstdc++

.PHONY: clean
clean:
	rm -rf build2 _sass.so

