# Reconciliation against USAspending — 2026-11-16T20:36:26+00:00

R1 completeness: 30 cells re-counted now, 26 exact, 4 with a delta, 0 beyond the 0.5% tolerance. R2 window sums: 50 sampled awards, 0 mismatches. R3 agency-year vs spending_over_time: 30 available, 4 with a non-zero delta, 0 beyond tolerance, 0 dollar differences on cells whose row count was exact. **PASS** (R2 must be exact to the cent; R1 and R3 deltas must stay within 0.5%; a cell with an exact row count must also match in dollars exactly; R3 grain: spending_over_time, spending_level=transactions, group=month, summed over the FY window (confirmed 2026-10-24)).

| check | agency | FY | ours | API | delta / match |
|---|---|---|---|---|---|
| R1 count | 013 | 2022 | 3,905 | 3905 | 0 |
| R1 count | 013 | 2023 | 3,469 | 3469 | 0 |
| R1 count | 013 | 2024 | 2,925 | 2925 | 0 |
| R1 count | 013 | 2025 | 2,653 | 2653 | 0 |
| R1 count | 013 | 2026 | 2,152 | 2152 | 0 |
| R1 count | 020 | 2022 | 3,822 | 3822 | 0 |
| R1 count | 020 | 2023 | 3,308 | 3309 | -1 |
| R1 count | 020 | 2024 | 3,372 | 3375 | -3 |
| R1 count | 020 | 2025 | 4,020 | 4022 | -2 |
| R1 count | 020 | 2026 | 2,868 | 2875 | -7 |
| R1 count | 028 | 2022 | 438 | 438 | 0 |
| R1 count | 028 | 2023 | 378 | 378 | 0 |
| R1 count | 028 | 2024 | 369 | 369 | 0 |
| R1 count | 028 | 2025 | 313 | 313 | 0 |
| R1 count | 028 | 2026 | 235 | 235 | 0 |
| R1 count | 036 | 2022 | 5,197 | 5197 | 0 |
| R1 count | 036 | 2023 | 4,265 | 4265 | 0 |
| R1 count | 036 | 2024 | 3,966 | 3966 | 0 |
| R1 count | 036 | 2025 | 3,912 | 3912 | 0 |
| R1 count | 036 | 2026 | 4,373 | 4373 | 0 |
| R1 count | 070 | 2022 | 8,020 | 8020 | 0 |
| R1 count | 070 | 2023 | 6,654 | 6654 | 0 |
| R1 count | 070 | 2024 | 5,502 | 5502 | 0 |
| R1 count | 070 | 2025 | 5,042 | 5042 | 0 |
| R1 count | 070 | 2026 | 4,457 | 4457 | 0 |
| R1 count | 075 | 2022 | 5,944 | 5944 | 0 |
| R1 count | 075 | 2023 | 5,465 | 5465 | 0 |
| R1 count | 075 | 2024 | 4,842 | 4842 | 0 |
| R1 count | 075 | 2025 | 4,311 | 4311 | 0 |
| R1 count | 075 | 2026 | 3,743 | 3743 | 0 |
| R2 award `CONT_AWD_HHSN268201700276U_7529_GS35F0119Y_4732` | 075 | 2026 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $539076.12) | match |
| R2 award `CONT_AWD_70Z02722PC0002673_7008_-NONE-_-NONE-` | 070 | 2022 | 1 tx, $5,769.84 | 1 tx, $5,769.84 (lifetime $9627.45) | match |
| R2 award `CONT_AWD_36C10B26N10030037_3600_VA11816D1003_3600` | 036 | 2026 | 3 tx, $8,657,621.89 | 3 tx, $8,657,621.89 (lifetime $8657621.89) | match |
| R2 award `CONT_AWD_70B04C21F00001029_7014_70B04C20A00000016_7014` | 070 | 2022 | 2 tx, $1,334.05 | 2 tx, $1,334.05 (lifetime $2713.59) | match |
| R2 award `CONT_AWD_20380223F00002_2036_47QTCA19D00GQ_4732` | 020 | 2023 | 1 tx, $10,385.22 | 1 tx, $10,385.22 (lifetime $10385.22) | match |
| R2 award `CONT_AWD_36C10A24F0031_3600_NNG15SD34B_8000` | 036 | 2024 | 2 tx, $661,790.07 | 2 tx, $661,790.07 (lifetime $661790.07) | match |
| R2 award `CONT_AWD_36C24120C0018_3600_-NONE-_-NONE-` | 036 | 2025 | 1 tx, $50,000.00 | 1 tx, $50,000.00 (lifetime $781626.25) | match |
| R2 award `CONT_AWD_75A50325P00010_7505_-NONE-_-NONE-` | 075 | 2025 | 1 tx, $9,838.50 | 1 tx, $9,838.50 (lifetime $20464.08) | match |
| R2 award `CONT_AWD_2023H225F00147_2050_47QTCA19D00CX_4732` | 020 | 2026 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $73189.52) | match |
| R2 award `CONT_AWD_DOCEA133W17CQ0082T0002_1330_DOCEA133W17CQ0082_1330` | 013 | 2024 | 7 tx, $3,123,666.00 | 7 tx, $3,123,666.00 (lifetime $31337327.15) | match |
| R2 award `CONT_AWD_70RCSJ24FR0000053_7001_47QTCB22D0276_4732` | 070 | 2025 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $510322.73) | match |
| R2 award `CONT_AWD_36C10B23F0239_3600_NNG15SD00B_8000` | 036 | 2023 | 1 tx, $128,556.28 | 1 tx, $128,556.28 (lifetime $123237.44) | match |
| R2 award `CONT_AWD_75A50222F62001_7505_75A50222A00002_7505` | 075 | 2026 | 1 tx, $2,142,857.94 | 1 tx, $2,142,857.94 (lifetime $8751931.36) | match |
| R2 award `CONT_AWD_1331L522P13210085_1301_-NONE-_-NONE-` | 013 | 2022 | 1 tx, $17,820.00 | 1 tx, $17,820.00 (lifetime $91979.64) | match |
| R2 award `CONT_AWD_70B06C24F00000501_7014_70RTAC21D00000001_7001` | 070 | 2024 | 1 tx, $12,987.88 | 1 tx, $12,987.88 (lifetime $12095.92) | match |
| R2 award `CONT_AWD_36C25025F0633_3600_47QTCA23D005Q_4732` | 036 | 2025 | 1 tx, $121,572.73 | 1 tx, $121,572.73 (lifetime $121572.73) | match |
| R2 award `CONT_AWD_20340623F00029_2036_NNG15SD60B_8000` | 020 | 2026 | 1 tx, $90,312.81 | 1 tx, $90,312.81 (lifetime $335004.29) | match |
| R2 award `CONT_AWD_36C26226P1422_3600_-NONE-_-NONE-` | 036 | 2026 | 1 tx, $29,170.32 | 1 tx, $29,170.32 (lifetime $29170.32) | match |
| R2 award `CONT_AWD_2032H522F00060_2050_47QTCK18D0014_4732` | 020 | 2022 | 12 tx, $5,596,445.17 | 12 tx, $5,596,445.17 (lifetime $5493115.79) | match |
| R2 award `CONT_AWD_2032H823F00221_2050_NNG15SC71B_8000` | 020 | 2026 | 1 tx, $32,964.00 | 1 tx, $32,964.00 (lifetime $131856.0) | match |
| R2 award `CONT_AWD_75D30121P12822_7523_-NONE-_-NONE-` | 075 | 2024 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $287952.0) | match |
| R2 award `CONT_AWD_70T03019F3BOGS009_7013_GS00Q17GWD2293_4732` | 070 | 2025 | 1 tx, $-32.84 | 1 tx, $-32.84 (lifetime $1888776.64) | match |
| R2 award `CONT_AWD_70FA3123F00000043_7022_70FA3019D00000003_7022` | 070 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $1708038.87) | match |
| R2 award `CONT_AWD_20341122F00016_2036_47QTCA20D00B5_4732` | 020 | 2023 | 1 tx, $252,000.00 | 1 tx, $252,000.00 (lifetime $1552742.96) | match |
| R2 award `CONT_AWD_28321320P00050036_2800_-NONE-_-NONE-` | 028 | 2022 | 1 tx, $52,500.00 | 1 tx, $52,500.00 (lifetime $270000.0) | match |
| R2 award `CONT_AWD_75F40119F19046_7524_HHSF223201610046I_7524` | 075 | 2023 | 1 tx, $-4,116.51 | 1 tx, $-4,116.51 (lifetime $335358.69) | match |
| R2 award `CONT_AWD_20340921P00118_2036_-NONE-_-NONE-` | 020 | 2024 | 1 tx, $1,548.61 | 1 tx, $1,548.61 (lifetime $107225.86) | match |
| R2 award `CONT_AWD_HHSM500201500341P_7530_-NONE-_-NONE-` | 075 | 2024 | 1 tx, $-3,092.56 | 1 tx, $-3,092.56 (lifetime $168092.53) | match |
| R2 award `CONT_AWD_75D30124F00001_7523_75D30124D19687_7523` | 075 | 2024 | 1 tx, $1,529,783.83 | 1 tx, $1,529,783.83 (lifetime $1529783.83) | match |
| R2 award `CONT_AWD_HSTS0217COIA173_7013_-NONE-_-NONE-` | 070 | 2024 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $714769.92) | match |
| R2 award `CONT_AWD_36C10B19F2964_3600_N0024418D0003_9700` | 036 | 2022 | 6 tx, $2,544.61 | 6 tx, $2,544.61 (lifetime $6616006.25) | match |
| R2 award `CONT_AWD_1331L521F13230297_1323_1331L519A13ES0038_1301` | 013 | 2025 | 1 tx, $-186.89 | 1 tx, $-186.89 (lifetime $70393.07) | match |
| R2 award `CONT_AWD_28321323FDX030214_2800_NNG15SD70B_8000` | 028 | 2023 | 1 tx, $622,878.70 | 1 tx, $622,878.70 (lifetime $622878.7) | match |
| R2 award `CONT_AWD_HSCETE11J00299_7012_HSHQDC09A00032_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $60499.2) | match |
| R2 award `CONT_AWD_70RDA125FR0000027_7001_70RTAC21D00000006_7001` | 070 | 2025 | 2 tx, $1,157,568.53 | 2 tx, $1,157,568.53 (lifetime $3037604.65) | match |
| R2 award `CONT_AWD_20341424F00028_2036_2032H521A00022_2050` | 020 | 2024 | 1 tx, $61,152.28 | 1 tx, $61,152.28 (lifetime $213792.28) | match |
| R2 award `CONT_AWD_HHSF223201710217A_7524_-NONE-_-NONE-` | 075 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $125099.36) | match |
| R2 award `CONT_AWD_75H71219P00049_7527_-NONE-_-NONE-` | 075 | 2023 | 1 tx, $5,500.00 | 1 tx, $5,500.00 (lifetime $30500.0) | match |
| R2 award `CONT_AWD_70US0922F3OTH2217_7009_75N98120D00179_7529` | 070 | 2022 | 2 tx, $712,741.23 | 2 tx, $712,741.23 (lifetime $0.0) | match |
| R2 award `CONT_AWD_VA11816F1616_3600_GS35F0170K_4730` | 036 | 2022 | 1 tx, $-176,823.95 | 1 tx, $-176,823.95 (lifetime $1014661.55) | match |
| R2 award `CONT_AWD_75H70420F80004_7527_GS35F0119P_4730` | 075 | 2022 | 3 tx, $427,611.95 | 3 tx, $427,611.95 (lifetime $1838366.23) | match |
| R2 award `CONT_AWD_70RTAC24FR0000069_7001_70RTAC21D00000006_7001` | 070 | 2024 | 1 tx, $127,380.16 | 1 tx, $127,380.16 (lifetime $127380.16) | match |
| R2 award `CONT_AWD_70Z03824FM0000035_7008_NNG15SC03B_8000` | 070 | 2024 | 2 tx, $65,168.40 | 2 tx, $65,168.40 (lifetime $65168.4) | match |
| R2 award `CONT_AWD_20340924P00003_2036_-NONE-_-NONE-` | 020 | 2024 | 1 tx, $40,703.00 | 1 tx, $40,703.00 (lifetime $164267.0) | match |
| R2 award `CONT_AWD_75F40123F19001_7524_75F40123A00032_7524` | 075 | 2023 | 1 tx, $138,071.76 | 1 tx, $138,071.76 (lifetime $107111.22) | match |
| R2 award `CONT_AWD_1331L523FNB130020_1341_NNG15SD68B_8000` | 013 | 2025 | 1 tx, $4,037.60 | 1 tx, $4,037.60 (lifetime $19640.24) | match |
| R2 award `CONT_AWD_36C24821F0038_3600_GS35F0408X_4732` | 036 | 2024 | 2 tx, $74,317.22 | 2 tx, $74,317.22 (lifetime $376764.27) | match |
| R2 award `CONT_AWD_HSCETE12F00191_7012_HSHQDC09A00032_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $22594.8) | match |
| R2 award `CONT_AWD_70T01020P7NOTD212_7013_-NONE-_-NONE-` | 070 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $146958.3) | match |
| R2 award `CONT_AWD_36C24521P0200_3600_-NONE-_-NONE-` | 036 | 2024 | 1 tx, $43,495.00 | 1 tx, $43,495.00 (lifetime $212450.0) | match |
| R3 agency-year | 013 | 2022 | $1,173,544,861.68 | $1,173,544,861.68 | 0.00 |
| R3 agency-year | 013 | 2023 | $1,315,663,689.24 | $1,315,663,689.24 | 0.00 |
| R3 agency-year | 013 | 2024 | $1,387,577,676.82 | $1,387,577,676.82 | 0.00 |
| R3 agency-year | 013 | 2025 | $1,358,090,856.19 | $1,358,090,856.19 | 0.00 |
| R3 agency-year | 013 | 2026 | $1,640,191,267.90 | $1,640,191,267.90 | 0.00 |
| R3 agency-year | 020 | 2022 | $1,819,975,487.12 | $1,819,975,487.12 | 0.00 |
| R3 agency-year | 020 | 2023 | $2,243,192,310.47 | $2,243,255,482.39 | -63,171.92 (row count short — see R1) |
| R3 agency-year | 020 | 2024 | $2,675,734,665.92 | $2,675,856,879.12 | -122,213.20 (row count short — see R1) |
| R3 agency-year | 020 | 2025 | $3,190,617,744.96 | $3,190,699,459.36 | -81,714.40 (row count short — see R1) |
| R3 agency-year | 020 | 2026 | $2,297,258,761.96 | $2,298,281,936.04 | -1,023,174.08 (row count short — see R1) |
| R3 agency-year | 028 | 2022 | $1,004,831,340.74 | $1,004,831,340.74 | 0.00 |
| R3 agency-year | 028 | 2023 | $1,052,732,490.79 | $1,052,732,490.79 | 0.00 |
| R3 agency-year | 028 | 2024 | $938,381,084.59 | $938,381,084.59 | 0.00 |
| R3 agency-year | 028 | 2025 | $781,780,087.36 | $781,780,087.36 | 0.00 |
| R3 agency-year | 028 | 2026 | $1,057,911,411.10 | $1,057,911,411.10 | 0.00 |
| R3 agency-year | 036 | 2022 | $6,730,049,177.23 | $6,730,049,177.23 | 0.00 |
| R3 agency-year | 036 | 2023 | $6,198,415,946.61 | $6,198,415,946.61 | 0.00 |
| R3 agency-year | 036 | 2024 | $6,872,839,324.71 | $6,872,839,324.71 | 0.00 |
| R3 agency-year | 036 | 2025 | $7,218,405,908.15 | $7,218,405,908.15 | 0.00 |
| R3 agency-year | 036 | 2026 | $8,593,829,210.84 | $8,593,829,210.84 | 0.00 |
| R3 agency-year | 070 | 2022 | $3,776,449,747.57 | $3,776,449,747.57 | 0.00 |
| R3 agency-year | 070 | 2023 | $4,149,874,995.92 | $4,149,874,995.92 | 0.00 |
| R3 agency-year | 070 | 2024 | $4,580,168,576.98 | $4,580,168,576.98 | 0.00 |
| R3 agency-year | 070 | 2025 | $4,594,607,687.63 | $4,594,607,687.63 | 0.00 |
| R3 agency-year | 070 | 2026 | $5,816,784,543.82 | $5,816,784,543.82 | 0.00 |
| R3 agency-year | 075 | 2022 | $5,518,703,581.60 | $5,518,703,581.60 | 0.00 |
| R3 agency-year | 075 | 2023 | $5,455,504,166.39 | $5,455,504,166.39 | 0.00 |
| R3 agency-year | 075 | 2024 | $5,513,022,707.43 | $5,513,022,707.43 | 0.00 |
| R3 agency-year | 075 | 2025 | $5,208,060,796.89 | $5,208,060,796.89 | 0.00 |
| R3 agency-year | 075 | 2026 | $5,697,146,007.06 | $5,697,146,007.06 | 0.00 |
