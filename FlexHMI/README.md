# FlexHMI
`FlexHMI`는 MQTT 프로토콜을 사용하여, PLC의 데이터에 접근 할 수 있는, 소스입니다.

MQTT 브로커 서버가 요구되지만, HMI는 이더넷 환경만 연결되어있다면, 서버가 요구되지 않습니다.

---

### 토픽 구조

`SESSION` : PLC를 사용하고 있는 고유 세션 이름입니다.<br>
`PLC_ID` : 세션에서 사용하고 있는 PLC의 고유 ID입니다.<br>
`ADDRESS` : 접근 할 PLC 주소입니다.<br>

- 입력
> flexflow/`SESSION`/`PLC_ID`/INPUT/`ADDRESS`

- 출력
> flexflow/`SESSION`/`PLC_ID`/OUTPUT/`ADDRESS`

- 내부 메모리
> flexflow/`SESSION`/`PLC_ID`/MEMORY/`ADDRESS`

---

### 토픽 구조 예시

- %IX0.1 접근
> flexflow/asm/rpi01/INPUT/0x1

- %QX1.2 접근
> flexflow/asm/rpi01/OUTPUT/1x2

- %MX0.7 접근
> flexflow/asm/rpi01/MEMORY/0x7