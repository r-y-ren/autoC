// NRF24 数传被测链路固件（桩阶段：结构+标记）
// 职责：RF24 定长包回环 → ARC_CNT/PLOS_CNT 丢包重传统计 → 1Hz JSON 串口上报（无 RSSI）
#include <Arduino.h>
#include "protocol.h"

static const char *FW_VERSION = "nrf24_link-0.0.1";

void setup() {
  Serial.begin(PROTOCOL_BAUD);
  // unimplemented:fn:nrf24_link_init（RF24 初始化 + SPI/VSPI 引脚 + 回环角色）
  // unimplemented:fn:nrf24_loop_traffic（定长包收发与 ARC_CNT/PLOS_CNT 读取）
}

void loop() {
  // unimplemented:fn:emit_sample      （组装 DutSample JSON 行并 Serial.println）
  delay(1000 / REPORT_HZ);
}
