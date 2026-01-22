# KOMETA (ZMK)

 Конфигурация ZMK для клавиатуры **KOMETA**.

## Важно

 Эта прошивка рассчитана на работу **только с донглом** (централью). **Без донгла прошивка не работает.**

 Донгл можно купить на AliExpress:

 <https://ali.click/svpswl>

 Или найти по запросу: `split dongle`.

## Сборка

 Список целей для сборки находится в `build.yaml`:

- `nice_nano` + `kometa_left`
- `nice_nano` + `kometa_right`
- `nice_nano` + `kometa_dongle dongle_display`

## Раскладка

### DEF

|      ESC       |   Q   |   W   |   E   |   R   |    T    |       |                 |    Y    |     U     |   I   |   O   |   P   | LALT  |
| :------------: | :---: | :---: | :---: | :---: | :-----: | :---: | :-------------: | :-----: | :-------: | :---: | :---: | :---: | :---: |
| MT(LSHIFT,TAB) |   A   |   S   |   D   |   F   |    G    |       |                 |    H    |     J     |   K   |   L   | SEMI  | LBKT  |
|      LGUI      |   Z   |   X   |   C   |   V   |    B    |       |                 |    N    |     M     | COMMA |  DOT  | FSLH  |  SQT  |
|                |       |       |       | LCTRL | MO(RSE) | SPACE | MT(RSHFT,ENTER) | MO(LWR) | BACKSPACE |       |       |       |       |

### WOW

|  ESC  |   Q   |   W   |   E   |   R   |   T   |       |                 |    Y    |     U     |   I   |   O   |   P   |      LBKT       |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :-------------: | :-----: | :-------: | :---: | :---: | :---: | :-------------: |
|  TAB  |   A   |   S   |   D   |   F   |   G   |       |                 |    H    |     J     |   K   |   L   | SEMI  |       SQT       |
| LSHFT |   Z   |   X   |   C   |   V   |   B   |       |                 |    N    |     M     | COMMA |  DOT  | FSLH  | MT(RSHFT,ENTER) |
|       |       |       |       |  N9   |  N7   | SPACE | MT(RSHFT,ENTER) | MO(LWR) | BACKSPACE |       |       |       |                 |

### FPS

|  ESC  |   Q   |   W   |   E   |   R   |     T     |       |       |    Y    |   U   |   I   |   O   |   P   |      LBKT       |
| :---: | :---: | :---: | :---: | :---: | :-------: | :---: | :---: | :-----: | :---: | :---: | :---: | :---: | :-------------: |
|  TAB  |   A   |   S   |   D   |   F   |     G     |       |       |    H    |   J   |   K   |   L   | SEMI  |       SQT       |
| LSHFT |   Z   |   X   |   C   |   V   |     B     |       |       |    N    |   M   | COMMA |  DOT  | FSLH  | MT(RSHFT,ENTER) |
|       |       |       |       |   M   | MO(LCTRL) | SPACE | ENTER | MO(LWR) |  F1   |       |       |       |                 |

### LWR

| OUT(OUT_TOG) | BT(BT_SEL,0) | BT(BT_SEL,1) | BT(BT_SEL,2) | BT(BT_SEL,3) | bt BT_CLR |       |       |  PAGE_UP  | LG(TAB) |  UP   | TRNS  | LA(F10) | studio_unlock |
| :----------: | :----------: | :----------: | :----------: | :----------: | :-------: | :---: | :---: | :-------: | :-----: | :---: | :---: | :-----: | :-----------: |
|     TRNS     |     TRNS     |     TRNS     |     TRNS     |     TRNS     | CAPSLOCK  |       |       | PAGE_DOWN |  LEFT   | DOWN  | RIGHT |  TRNS   |   TOG(FPS)    |
|     TRNS     |     TRNS     |     TRNS     |     TRNS     |     TRNS     |   TRNS    |       |       |   TRNS    |  HOME   | TRNS  |  END  |  TRNS   |   TOG(WOW)    |
|              |              |              |              |     TRNS     |   TRNS    | TRNS  | TRNS  |   TRNS    | DELETE  |       |       |         |               |

### RSE

| boot_esc 0 ESC |  F1   |       F2        |  F3   |  F4   |  F5   |       |       |  F6   |  F7   |    F8    |    F9    |    F10    | TRNS  |
| :------------: | :---: | :-------------: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :------: | :------: | :-------: | :---: |
|      F12       |  N1   |       N2        |  N3   |  N4   |  N5   |       |       |  N6   |  N7   |    N8    |    N9    |    N0     |  F11  |
|      TRNS      | EQUAL | MT(UNDER,MINUS) | PLUS  | LBRC  | RBRC  |       |       | LBKT  | RBKT  | C_VOL_DN | C_VOL_UP | BACKSLASH | GRAVE |
|                |       |                 |       | LALT  | TRNS  | TRNS  | TRNS  | TRNS  | TRNS  |          |          |           |       |
