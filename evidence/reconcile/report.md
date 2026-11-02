# Reconciliation against USAspending — 2026-11-02T20:23:55+00:00

R1 completeness: 30 cells re-counted now, 26 exact, 4 with a delta, 0 beyond the 0.5% tolerance. R2 window sums: 50 sampled awards, 0 mismatches. R3 agency-year vs spending_over_time: 30 available, 4 with a non-zero delta, 0 beyond tolerance, 0 dollar differences on cells whose row count was exact. **PASS** (R2 must be exact to the cent; R1 and R3 deltas must stay within 0.5%; a cell with an exact row count must also match in dollars exactly; R3 grain: spending_over_time, spending_level=transactions, group=month, summed over the FY window (confirmed 2026-10-24)).

| check | agency | FY | ours | API | delta / match |
|---|---|---|---|---|---|
| R1 count | 013 | 2022 | 3,898 | 3898 | 0 |
| R1 count | 013 | 2023 | 3,463 | 3463 | 0 |
| R1 count | 013 | 2024 | 2,907 | 2907 | 0 |
| R1 count | 013 | 2025 | 2,638 | 2638 | 0 |
| R1 count | 013 | 2026 | 2,152 | 2152 | 0 |
| R1 count | 020 | 2022 | 3,822 | 3822 | 0 |
| R1 count | 020 | 2023 | 3,308 | 3309 | -1 |
| R1 count | 020 | 2024 | 3,372 | 3375 | -3 |
| R1 count | 020 | 2025 | 4,020 | 4022 | -2 |
| R1 count | 020 | 2026 | 2,865 | 2871 | -6 |
| R1 count | 028 | 2022 | 438 | 438 | 0 |
| R1 count | 028 | 2023 | 378 | 378 | 0 |
| R1 count | 028 | 2024 | 369 | 369 | 0 |
| R1 count | 028 | 2025 | 313 | 313 | 0 |
| R1 count | 028 | 2026 | 235 | 235 | 0 |
| R1 count | 036 | 2022 | 5,197 | 5197 | 0 |
| R1 count | 036 | 2023 | 4,268 | 4268 | 0 |
| R1 count | 036 | 2024 | 3,972 | 3972 | 0 |
| R1 count | 036 | 2025 | 3,917 | 3917 | 0 |
| R1 count | 036 | 2026 | 4,382 | 4382 | 0 |
| R1 count | 070 | 2022 | 8,020 | 8020 | 0 |
| R1 count | 070 | 2023 | 6,654 | 6654 | 0 |
| R1 count | 070 | 2024 | 5,502 | 5502 | 0 |
| R1 count | 070 | 2025 | 5,040 | 5040 | 0 |
| R1 count | 070 | 2026 | 4,451 | 4451 | 0 |
| R1 count | 075 | 2022 | 5,944 | 5944 | 0 |
| R1 count | 075 | 2023 | 5,465 | 5465 | 0 |
| R1 count | 075 | 2024 | 4,842 | 4842 | 0 |
| R1 count | 075 | 2025 | 4,310 | 4310 | 0 |
| R1 count | 075 | 2026 | 3,743 | 3743 | 0 |
| R2 award `CONT_AWD_70RSAT24FC0000005_7001_70RSAT22A00000001_7001` | 070 | 2024 | 3 tx, $9,561,762.46 | 3 tx, $9,561,762.46 (lifetime $11858735.36) | match |
| R2 award `CONT_AWD_36C10B24F0335_3600_47QTCA20D000W_4732` | 036 | 2025 | 1 tx, $10,039,451.38 | 1 tx, $10,039,451.38 (lifetime $28886990.36) | match |
| R2 award `CONT_AWD_1332KQ21FNEEB0007_1330_47QTCA19D00CX_4732` | 013 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $17959.9) | match |
| R2 award `CONT_AWD_36C24523C0090_3600_-NONE-_-NONE-` | 036 | 2026 | 3 tx, $108,790.30 | 3 tx, $108,790.30 (lifetime $395817.7) | match |
| R2 award `CONT_AWD_70FA3019F00000315_7022_70FA3018D00000003_7022` | 070 | 2025 | 1 tx, $-594.32 | 1 tx, $-594.32 (lifetime $14379.47) | match |
| R2 award `CONT_AWD_75H71120F80095_7527_36F79719D0135_3600` | 075 | 2025 | 1 tx, $-936.00 | 1 tx, $-936.00 (lifetime $18762.06) | match |
| R2 award `CONT_AWD_2032H524F00696_2050_GS35F328GA_4732` | 020 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $73828.39) | match |
| R2 award `CONT_AWD_36C25626P0158_3600_-NONE-_-NONE-` | 036 | 2026 | 1 tx, $35,465.00 | 1 tx, $35,465.00 (lifetime $35465.0) | match |
| R2 award `CONT_AWD_HSCETE17J00055_7012_HSCETE11A00002_7012` | 070 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $22856.48) | match |
| R2 award `CONT_AWD_70FA3020F00000295_7022_70FA3018D00000002_7022` | 070 | 2024 | 1 tx, $-126.60 | 1 tx, $-126.60 (lifetime $216.48) | match |
| R2 award `CONT_AWD_36C10B25F0181_3600_47QTCA21D00C1_4732` | 036 | 2025 | 2 tx, $868,720.32 | 2 tx, $868,720.32 (lifetime $1766526.24) | match |
| R2 award `CONT_AWD_70FBTX24F00000027_7022_70FBTX23A00000002_7022` | 070 | 2025 | 1 tx, $-3,630.15 | 1 tx, $-3,630.15 (lifetime $1121.85) | match |
| R2 award `CONT_AWD_36C24123P0294_3600_-NONE-_-NONE-` | 036 | 2025 | 1 tx, $15,750.00 | 1 tx, $15,750.00 (lifetime $64050.0) | match |
| R2 award `CONT_AWD_75D30126F20756_7523_HHSN316201200182W_7529` | 075 | 2026 | 3 tx, $1,958,855.37 | 3 tx, $1,958,855.37 (lifetime $1958855.37) | match |
| R2 award `CONT_AWD_2031JW23F00128_2046_NNG15SC71B_8000` | 020 | 2023 | 1 tx, $87,421.27 | 1 tx, $87,421.27 (lifetime $87421.27) | match |
| R2 award `CONT_AWD_20342820F00003_2036_NNG15SD12B_8000` | 020 | 2023 | 1 tx, $-3,734.62 | 1 tx, $-3,734.62 (lifetime $10093.55) | match |
| R2 award `CONT_AWD_36C24922P0722_3600_-NONE-_-NONE-` | 036 | 2023 | 1 tx, $98,881.16 | 1 tx, $98,881.16 (lifetime $495306.02) | match |
| R2 award `CONT_AWD_75A50119F80035_7505_GS35F0297K_4730` | 075 | 2022 | 2 tx, $10,094.96 | 2 tx, $10,094.96 (lifetime $204313.1) | match |
| R2 award `CONT_AWD_70FBR022F00000028_7022_70FA3018D00000003_7022` | 070 | 2024 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $300.85) | match |
| R2 award `CONT_AWD_75Q80125F80004_7528_47QTCA18D00AU_4732` | 075 | 2025 | 2 tx, $2,905,370.00 | 2 tx, $2,905,370.00 (lifetime $6579207.8) | match |
| R2 award `CONT_AWD_36C10B24C0055_3600_-NONE-_-NONE-` | 036 | 2025 | 1 tx, $66,605.21 | 1 tx, $66,605.21 (lifetime $4788888.49) | match |
| R2 award `CONT_AWD_36C24720F0857_3600_NNG15SD19B_8000` | 036 | 2022 | 2 tx, $-51,797.67 | 2 tx, $-51,797.67 (lifetime $1475945.18) | match |
| R2 award `CONT_AWD_75N98020F00001_7529_HHSN316201300006W_7529` | 075 | 2022 | 2 tx, $59,704.11 | 2 tx, $59,704.11 (lifetime $309102.46) | match |
| R2 award `CONT_AWD_36C24919F0159_3600_NNG15SD22B_8000` | 036 | 2023 | 1 tx, $75,995.26 | 1 tx, $75,995.26 (lifetime $2412159.45) | match |
| R2 award `CONT_AWD_VA11816F10060010_3600_VA11816D1006_3600` | 036 | 2022 | 1 tx, $-74,429.87 | 1 tx, $-74,429.87 (lifetime $27952199.22) | match |
| R2 award `CONT_AWD_1332KP21PNEEB0062_1330_-NONE-_-NONE-` | 013 | 2023 | 2 tx, $1,047,610.77 | 2 tx, $1,047,610.77 (lifetime $5236019.99) | match |
| R2 award `CONT_AWD_70CMSD23P00000124_7012_-NONE-_-NONE-` | 070 | 2024 | 1 tx, $1,000,000.00 | 1 tx, $1,000,000.00 (lifetime $3000000.0) | match |
| R2 award `CONT_AWD_75N91022P00479_7529_-NONE-_-NONE-` | 075 | 2022 | 1 tx, $12,998.00 | 1 tx, $12,998.00 (lifetime $12998.0) | match |
| R2 award `CONT_AWD_36C25222C0059_3600_-NONE-_-NONE-` | 036 | 2025 | 1 tx, $24,000.00 | 1 tx, $24,000.00 (lifetime $112600.0) | match |
| R2 award `CONT_AWD_70Z07919FPT111300_7008_GS00Q17GWD2169_4732` | 070 | 2022 | 1 tx, $152,486.40 | 1 tx, $152,486.40 (lifetime $730571.23) | match |
| R2 award `CONT_AWD_70B04C20P00000438_7014_-NONE-_-NONE-` | 070 | 2024 | 1 tx, $4,715.60 | 1 tx, $4,715.60 (lifetime $9431.2) | match |
| R2 award `CONT_AWD_36C10B20F0195_3600_NNG15SD22B_8000` | 036 | 2022 | 1 tx, $339,368.40 | 1 tx, $339,368.40 (lifetime $5832892.1) | match |
| R2 award `CONT_AWD_36C10B25C0059_3600_-NONE-_-NONE-` | 036 | 2026 | 3 tx, $326,786.76 | 3 tx, $326,786.76 (lifetime $541314.04) | match |
| R2 award `CONT_AWD_140D0426P8043_1406_-NONE-_-NONE-` | 020 | 2023 | 1 tx, $16,200.00 | 1 tx, $16,200.00 (lifetime $61620.0) | match |
| R2 award `CONT_AWD_HSCETE15F00088_7012_HSHQDC15A00017_7001` | 070 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $29757.72) | match |
| R2 award `CONT_AWD_1333LC20F00000140_1323_GS00F178DA_4732` | 013 | 2022 | 3 tx, $126,216.00 | 3 tx, $126,216.00 (lifetime $792295.98) | match |
| R2 award `CONT_AWD_1331L519F13OS0715_1301_GS00Q17GWD2299_4732` | 013 | 2022 | 1 tx, $-16,993.83 | 1 tx, $-16,993.83 (lifetime $3595037.95) | match |
| R2 award `CONT_AWD_75F40122F19014_7524_75F40119A10017_7524` | 075 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $5048171.84) | match |
| R2 award `CONT_AWD_70T02020F1NPHY030_7013_70T02019A3NPHY002_7013` | 070 | 2025 | 1 tx, $-10.09 | 1 tx, $-10.09 (lifetime $61395.89) | match |
| R2 award `CONT_AWD_2032H820P00047_2050_-NONE-_-NONE-` | 020 | 2023 | 1 tx, $93,464.00 | 1 tx, $93,464.00 (lifetime $562789.31) | match |
| R2 award `CONT_AWD_36C25520N0416_3600_36C25520A0055_3600` | 036 | 2023 | 1 tx, $-109,287.21 | 1 tx, $-109,287.21 (lifetime $1477045.37) | match |
| R2 award `CONT_AWD_1331L522FNRMA0138_1301_DOCSS130118BU0005_1301` | 013 | 2022 | 1 tx, $15,975.46 | 1 tx, $15,975.46 (lifetime $15975.46) | match |
| R2 award `CONT_AWD_75N97019F00059_7529_75N97019A00009_7529` | 075 | 2022 | 1 tx, $-94,428.00 | 1 tx, $-94,428.00 (lifetime $123362.0) | match |
| R2 award `CONT_AWD_1305M224F0473_1330_1331L523D13OS0003_1301` | 013 | 2025 | 2 tx, $474,594.00 | 2 tx, $474,594.00 (lifetime $1066086.0) | match |
| R2 award `CONT_AWD_75F40120F80151_7524_GS30F0029Y_4732` | 075 | 2023 | 2 tx, $24,237.22 | 2 tx, $24,237.22 (lifetime $117718.87) | match |
| R2 award `CONT_AWD_1333ND22FNB180078_1341_NNG15SC69B_8000` | 013 | 2022 | 1 tx, $131,014.91 | 1 tx, $131,014.91 (lifetime $131014.91) | match |
| R2 award `CONT_AWD_70RFP320FREH00012_7001_70B06C19D00000005_7014` | 070 | 2023 | 2 tx, $684,890.06 | 2 tx, $684,890.06 (lifetime $6492125.19) | match |
| R2 award `CONT_AWD_20340926P00091_2036_-NONE-_-NONE-` | 020 | 2026 | 1 tx, $18,099.00 | 1 tx, $18,099.00 (lifetime $18099.0) | match |
| R2 award `CONT_AWD_70FBR124P00000010_7022_-NONE-_-NONE-` | 070 | 2026 | 1 tx, $-49.65 | 1 tx, $-49.65 (lifetime $6360.1) | match |
| R2 award `CONT_AWD_75H70622P00864_7527_-NONE-_-NONE-` | 075 | 2022 | 1 tx, $9,900.00 | 1 tx, $9,900.00 (lifetime $14850.0) | match |
| R3 agency-year | 013 | 2022 | $1,170,880,572.20 | $1,170,880,572.20 | 0.00 |
| R3 agency-year | 013 | 2023 | $1,314,026,936.94 | $1,314,026,936.94 | 0.00 |
| R3 agency-year | 013 | 2024 | $1,376,640,938.61 | $1,376,640,938.61 | 0.00 |
| R3 agency-year | 013 | 2025 | $1,354,182,418.21 | $1,354,182,418.21 | 0.00 |
| R3 agency-year | 013 | 2026 | $1,640,191,267.90 | $1,640,191,267.90 | 0.00 |
| R3 agency-year | 020 | 2022 | $1,819,975,487.12 | $1,819,975,487.12 | 0.00 |
| R3 agency-year | 020 | 2023 | $2,243,192,310.47 | $2,243,255,482.39 | -63,171.92 (row count short — see R1) |
| R3 agency-year | 020 | 2024 | $2,675,734,665.92 | $2,675,856,879.12 | -122,213.20 (row count short — see R1) |
| R3 agency-year | 020 | 2025 | $3,190,617,744.96 | $3,190,699,459.36 | -81,714.40 (row count short — see R1) |
| R3 agency-year | 020 | 2026 | $2,292,301,605.29 | $2,292,292,060.57 | 9,544.72 (row count short — see R1) |
| R3 agency-year | 028 | 2022 | $1,004,831,340.74 | $1,004,831,340.74 | 0.00 |
| R3 agency-year | 028 | 2023 | $1,052,732,490.79 | $1,052,732,490.79 | 0.00 |
| R3 agency-year | 028 | 2024 | $938,381,084.59 | $938,381,084.59 | 0.00 |
| R3 agency-year | 028 | 2025 | $781,780,087.36 | $781,780,087.36 | 0.00 |
| R3 agency-year | 028 | 2026 | $1,057,911,411.10 | $1,057,911,411.10 | 0.00 |
| R3 agency-year | 036 | 2022 | $6,730,049,177.23 | $6,730,049,177.23 | 0.00 |
| R3 agency-year | 036 | 2023 | $6,198,672,091.84 | $6,198,672,091.84 | 0.00 |
| R3 agency-year | 036 | 2024 | $6,873,035,010.42 | $6,873,035,010.42 | 0.00 |
| R3 agency-year | 036 | 2025 | $7,218,604,432.11 | $7,218,604,432.11 | 0.00 |
| R3 agency-year | 036 | 2026 | $8,594,542,121.90 | $8,594,542,121.90 | 0.00 |
| R3 agency-year | 070 | 2022 | $3,776,449,747.57 | $3,776,449,747.57 | 0.00 |
| R3 agency-year | 070 | 2023 | $4,149,874,995.92 | $4,149,874,995.92 | 0.00 |
| R3 agency-year | 070 | 2024 | $4,580,168,576.98 | $4,580,168,576.98 | 0.00 |
| R3 agency-year | 070 | 2025 | $4,594,614,260.48 | $4,594,614,260.48 | 0.00 |
| R3 agency-year | 070 | 2026 | $5,811,571,703.77 | $5,811,571,703.77 | 0.00 |
| R3 agency-year | 075 | 2022 | $5,518,703,581.60 | $5,518,703,581.60 | 0.00 |
| R3 agency-year | 075 | 2023 | $5,455,504,166.39 | $5,455,504,166.39 | 0.00 |
| R3 agency-year | 075 | 2024 | $5,513,022,707.43 | $5,513,022,707.43 | 0.00 |
| R3 agency-year | 075 | 2025 | $5,208,060,799.64 | $5,208,060,799.64 | 0.00 |
| R3 agency-year | 075 | 2026 | $5,697,146,007.06 | $5,697,146,007.06 | 0.00 |
