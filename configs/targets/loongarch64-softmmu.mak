TARGET_ARCH=loongarch64
TARGET_BASE_ARCH=loongarch
TARGET_SUPPORTS_MTTCG=y
TARGET_XML_FILES= gdb-xml/loongarch-base32.xml gdb-xml/loongarch-base64.xml gdb-xml/loongarch-fpu.xml
# all boards require libfdt
TARGET_NEED_FDT=y
