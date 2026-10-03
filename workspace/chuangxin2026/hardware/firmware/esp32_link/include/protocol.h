// 串口 JSON 契约常量（与 contracts/sw-hw-interface.md §2 一致；上位机=linkbench.dut）
#pragma once

#define PROTOCOL_BAUD 115200
#define LINK_ID_WIFI "wifi"
#define LINK_ID_NRF24 "nrf24"
#define REPORT_HZ 1

// JSON 字段名（上位机 DutSample 逐字段对应）
#define F_LINK "link"
#define F_SEQ "seq"
#define F_TS "ts_ms"
#define F_PER "per"
#define F_TXN "tx_n"
#define F_ERRN "err_n"
#define F_RSSI "rssi_dbm"   // 仅 wifi
#define F_ARC "arc_avg"     // 仅 nrf24
#define F_PLOS "plos_cnt"   // 仅 nrf24
#define F_FW "fw"
