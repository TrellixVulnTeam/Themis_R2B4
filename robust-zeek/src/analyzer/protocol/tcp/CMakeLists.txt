
include(ZeekPlugin)

include_directories(BEFORE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

zeek_plugin_begin(Zeek TCP)
zeek_plugin_cc(TCP.cc TCP_Endpoint.cc TCP_Reassembler.cc ContentLine.cc Stats.cc Plugin.cc TCP_Father.cc)
zeek_plugin_bif(events.bif)
zeek_plugin_bif(types.bif)
zeek_plugin_bif(functions.bif)
zeek_plugin_end()
