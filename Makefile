CC = gcc
CFLAGS = -Wall -Wextra -fPIC -lpthread -Wno-unused-command-line-argument
SRC_DIR = src
BUILD_DIR = build
TARGET = server
TEST_TARGET = test_server
PYTHON_TEST_SCRIPT = testing_server.py

SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))
SO_TARGETS = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/lib%.so,$(SRCS))

.PHONY: all clean test

all: $(BUILD_DIR)/$(TARGET)

$(BUILD_DIR)/$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.c $(SRC_DIR)/common.h
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/skt_conn.o: $(SRC_DIR)/skt_conn.c $(SRC_DIR)/common.h
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/pipe_comm.o: $(SRC_DIR)/pipe_comm.c $(SRC_DIR)/common.h
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/serve_file.o: $(SRC_DIR)/serve_file.c $(SRC_DIR)/common.h
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/router.o: $(SRC_DIR)/router.c $(SRC_DIR)/common.h  $(SRC_DIR)/pipe_comm.c $(SRC_DIR)/serve_file.c $(SRC_DIR)/skt_conn.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@


$(BUILD_DIR)/server.o: $(SRC_DIR)/server.c $(SRC_DIR)/router.c $(SRC_DIR)/common.h  $(SRC_DIR)/pipe_comm.c $(SRC_DIR)/serve_file.c $(SRC_DIR)/skt_conn.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@



$(BUILD_DIR)/libskt_conn.so: $(BUILD_DIR)/skt_conn.o
	$(CC) $(CFLAGS) -shared $< -o $@

$(BUILD_DIR)/libpipe_comm.so: $(BUILD_DIR)/pipe_comm.o
	$(CC) $(CFLAGS) -shared $< -o $@

$(BUILD_DIR)/libserve_file.so: $(BUILD_DIR)/serve_file.o
	$(CC) $(CFLAGS) -shared $< -o $@

$(BUILD_DIR)/librouter.so: $(BUILD_DIR)/router.o $(BUILD_DIR)/libpipe_comm.so $(BUILD_DIR)/libserve_file.so
	$(CC) $(CFLAGS) -shared $^ -o $@

$(BUILD_DIR)/libserver.so: $(BUILD_DIR)/server.o $(BUILD_DIR)/router.o $(BUILD_DIR)/libpipe_comm.so $(BUILD_DIR)/libserve_file.so $(BUILD_DIR)/libskt_conn.so
	$(CC) $(CFLAGS) -shared $^ -o $@

clean:
	rm -rf $(BUILD_DIR)

test:
	python3 $(PYTHON_TEST_SCRIPT)
