// ESP32 WiFi 被测链路固件（桩阶段：结构+标记，实现在 fn-implement）
// 职责：STA 模式收 UDP 定长流 → 统计 PER/重传/RSSI → 1Hz JSON 串口上报
#include <Arduino.h>
#include "protocol.h"

static const char *FW_VERSION = "esp32_link-0.0.1";

void setup() {
  Serial.begin(PROTOCOL_BAUD);
  // unimplemented:fn:wifi_link_init   （STA 关联 + UDP 流接收任务起）
  // unimplemented:fn:udp_stream_start （定长流收发与计数）
}

void loop() {
  // unimplemented:fn:emit_sample      （组装 DutSample JSON 行并 Serial.println）
  delay(1000 / REPORT_HZ);
}
