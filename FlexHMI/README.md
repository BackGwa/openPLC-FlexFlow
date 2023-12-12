# FlexHMI
`FlexHMI`는 MQTT 프로토콜을 사용하여, PLC의 데이터에 접근 할 수 있는, 소스입니다.

MQTT 브로커 서버가 요구되지만, HMI는 이더넷 환경만 연결되어있다면, 서버가 요구되지 않습니다.

FlexFlow의 장점은 무선 HMI를 구현 할 수 있으며,
언제 어디서 무선 연결이 가능한 디바이스를 활용하여, PLC를 컨트롤 할 수 있습니다.

---

### 토픽 구조

`SESSION` : PLC를 사용하고 있는 고유 세션 이름입니다.<br>
`PLC_ID` : 세션에서 사용하고 있는 PLC의 고유 ID입니다.<br>
`TYPE` : 자료형을 설정합니다. `INT`, `BOOL`, `STRING`, `REAL`이 지원됩니다.<br>
`ADDRESS` : 접근 할 PLC 주소입니다.<br>

- 입력
> flexflow/`SESSION`/`PLC_ID`/INPUT/`TYPE`/`ADDRESS`

- 출력
> flexflow/`SESSION`/`PLC_ID`/OUTPUT/`TYPE`/`ADDRESS`

- 내부 메모리
> flexflow/`SESSION`/`PLC_ID`/MEMORY/`TYPE`/`ADDRESS`

---

### 토픽 구조 예시

- %IX0.1 (BOOL) 접근
> flexflow/asm/rpi01/INPUT/BOOL/0x1

- %QX1.2 (BOOL) 접근
> flexflow/asm/rpi01/OUTPUT/BOOL/1x2

- %MX0.7 (INT) 접근
> flexflow/asm/rpi01/MEMORY/INT/0x7