# Reconciliation against USAspending — 2026-11-23T22:12:39+00:00

R1 completeness: 30 cells re-counted now, 26 exact, 4 with a delta, 0 beyond the 0.5% tolerance. R2 window sums: 50 sampled awards, 0 mismatches. R3 agency-year vs spending_over_time: 30 available, 4 with a non-zero delta, 0 beyond tolerance, 0 dollar differences on cells whose row count was exact. **PASS** (R2 must be exact to the cent; R1 and R3 deltas must stay within 0.5%; a cell with an exact row count must also match in dollars exactly; R3 grain: spending_over_time, spending_level=transactions, group=month, summed over the FY window (confirmed 2026-10-24)).

| check | agency | FY | ours | API | delta / match |
|---|---|---|---|---|---|
| R1 count | 013 | 2022 | 3,905 | 3905 | 0 |
| R1 count | 013 | 2023 | 3,469 | 3469 | 0 |
| R1 count | 013 | 2024 | 2,925 | 2925 | 0 |
| R1 count | 013 | 2025 | 2,653 | 2653 | 0 |
| R1 count | 013 | 2026 | 2,155 | 2155 | 0 |
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
| R1 count | 036 | 2025 | 3,917 | 3917 | 0 |
| R1 count | 036 | 2026 | 4,377 | 4377 | 0 |
| R1 count | 070 | 2022 | 8,020 | 8020 | 0 |
| R1 count | 070 | 2023 | 6,654 | 6654 | 0 |
| R1 count | 070 | 2024 | 5,502 | 5502 | 0 |
| R1 count | 070 | 2025 | 5,043 | 5043 | 0 |
| R1 count | 070 | 2026 | 4,459 | 4459 | 0 |
| R1 count | 075 | 2022 | 5,944 | 5944 | 0 |
| R1 count | 075 | 2023 | 5,465 | 5465 | 0 |
| R1 count | 075 | 2024 | 4,842 | 4842 | 0 |
| R1 count | 075 | 2025 | 4,311 | 4311 | 0 |
| R1 count | 075 | 2026 | 3,743 | 3743 | 0 |
| R2 award `CONT_AWD_70US0924P70092092_7009_-NONE-_-NONE-` | 070 | 2025 | 2 tx, $6,547.04 | 2 tx, $6,547.04 (lifetime $26592.58) | match |
| R2 award `CONT_AWD_HSCETE16J00140_7012_HSHQDC12D00014_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $14268.76) | match |
| R2 award `CONT_AWD_2032H324C00009_2001_-NONE-_-NONE-` | 020 | 2026 | 3 tx, $160,356.00 | 3 tx, $160,356.00 (lifetime $435398.0) | match |
| R2 award `CONT_AWD_70RTAC23FC0000022_7001_70RTAC21A00000011_7001` | 070 | 2023 | 4 tx, $1,231,465.90 | 4 tx, $1,231,465.90 (lifetime $1231465.9) | match |
| R2 award `CONT_AWD_70CMSD22P00000018_7012_-NONE-_-NONE-` | 070 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $71288.07) | match |
| R2 award `CONT_AWD_2032H824F00043_2050_47QTCB21D0289_4732` | 020 | 2024 | 3 tx, $2,136,758.55 | 3 tx, $2,136,758.55 (lifetime $2136756.55) | match |
| R2 award `CONT_AWD_75040124F46004_7504_75040121A00004_7504` | 075 | 2025 | 1 tx, $-271,694.28 | 1 tx, $-271,694.28 (lifetime $1810778.31) | match |
| R2 award `CONT_AWD_70T05024P5903N017_7013_-NONE-_-NONE-` | 070 | 2024 | 1 tx, $11,940.00 | 1 tx, $11,940.00 (lifetime $59420.0) | match |
| R2 award `CONT_AWD_2031JW21P00003_2046_-NONE-_-NONE-` | 020 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $115630.0) | match |
| R2 award `CONT_AWD_1331L524F0001_1301_1331L523A13ES0071_1301` | 013 | 2024 | 3 tx, $16,379.37 | 3 tx, $16,379.37 (lifetime $31941.1) | match |
| R2 award `CONT_AWD_1333LB19F00000392_1323_NNG15SC09B_8000` | 013 | 2022 | 1 tx, $51,534.41 | 1 tx, $51,534.41 (lifetime $274394.86) | match |
| R2 award `CONT_AWD_75N91024F00002_7529_HHSN316201500053W_7529` | 075 | 2024 | 2 tx, $35,698.51 | 2 tx, $35,698.51 (lifetime $35698.51) | match |
| R2 award `CONT_AWD_20343220F00015_2036_GS00Q17NSD3001_4732` | 020 | 2024 | 3 tx, $30,267.90 | 3 tx, $30,267.90 (lifetime $956362.34) | match |
| R2 award `CONT_AWD_36C24923F0032_3600_NNG15SD34B_8000` | 036 | 2023 | 1 tx, $10,800.01 | 1 tx, $10,800.01 (lifetime $59676.88) | match |
| R2 award `CONT_AWD_2032H320F00014_2001_2032H318D00002_2001` | 020 | 2022 | 1 tx, $11,985.36 | 1 tx, $11,985.36 (lifetime $18530.33) | match |
| R2 award `CONT_AWD_75N92E20F50002_7529_HHSN316201500043W_7529` | 075 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $10947.27) | match |
| R2 award `CONT_AWD_36C25623F0310_3600_NNG15SD22B_8000` | 036 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $609420.27) | match |
| R2 award `CONT_AWD_1331L524F0672_1301_1331L523A13ES0021_1301` | 013 | 2026 | 1 tx, $11,282.64 | 1 tx, $11,282.64 (lifetime $31908.12) | match |
| R2 award `CONT_AWD_2032H523F00059_2050_GS35F017CA_4732` | 020 | 2025 | 7 tx, $3,223,289.21 | 7 tx, $3,223,289.21 (lifetime $9198119.74) | match |
| R2 award `CONT_AWD_2033H626F00076_2036_2033H622D00003_2036` | 020 | 2026 | 1 tx, $1,317,071.60 | 1 tx, $1,317,071.60 (lifetime $1317071.6) | match |
| R2 award `CONT_AWD_1333ND23PNB640570_1341_-NONE-_-NONE-` | 013 | 2025 | 2 tx, $59,475.00 | 2 tx, $59,475.00 (lifetime $251215.0) | match |
| R2 award `CONT_AWD_70CMSD26P00000095_7012_-NONE-_-NONE-` | 070 | 2026 | 1 tx, $76,344.00 | 1 tx, $76,344.00 (lifetime $76344.0) | match |
| R2 award `CONT_AWD_70B04C26F00000527_7014_47QTCK18D0036_4732` | 070 | 2026 | 1 tx, $14,823,471.22 | 1 tx, $14,823,471.22 (lifetime $14823471.22) | match |
| R2 award `CONT_AWD_36C24719P0007_3600_-NONE-_-NONE-` | 036 | 2024 | 1 tx, $-10,942.00 | 1 tx, $-10,942.00 (lifetime $32826.0) | match |
| R2 award `CONT_AWD_75Q80119F32006_7528_HHSA290201600003I_7528` | 075 | 2022 | 1 tx, $-5.97 | 1 tx, $-5.97 (lifetime $399994.03) | match |
| R2 award `CONT_AWD_36C10B23N00060009_3600_36C10B21D0006_3600` | 036 | 2023 | 2 tx, $7,199,971.20 | 2 tx, $7,199,971.20 (lifetime $7199971.2) | match |
| R2 award `CONT_AWD_75N95D20F40008_7529_HHSN316201500043W_7529` | 075 | 2024 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $38846.65) | match |
| R2 award `CONT_AWD_70T03018F2BCIO853_7013_HSHQDC13D00021_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $39650000.0) | match |
| R2 award `CONT_AWD_2032H519F00120_2050_GS35F0494T_4730` | 020 | 2025 | 1 tx, $-53.84 | 1 tx, $-53.84 (lifetime $4942606.6) | match |
| R2 award `CONT_AWD_HHSP233201600050W_7555_NNG15SC27B_8000` | 075 | 2026 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $7969355.35) | match |
| R2 award `CONT_AWD_70FBR023F00000013_7022_70FA3018D00000002_7022` | 070 | 2023 | 1 tx, $285.90 | 1 tx, $285.90 (lifetime $285.9) | match |
| R2 award `CONT_AWD_36C24823P2476_3600_-NONE-_-NONE-` | 036 | 2023 | 1 tx, $105,904.00 | 1 tx, $105,904.00 (lifetime $105904.0) | match |
| R2 award `CONT_AWD_2032H521P00074_2050_-NONE-_-NONE-` | 020 | 2023 | 1 tx, $29,259.97 | 1 tx, $29,259.97 (lifetime $84539.91) | match |
| R2 award `CONT_AWD_2032H525C00035_2050_-NONE-_-NONE-` | 020 | 2026 | 1 tx, $428,832.00 | 1 tx, $428,832.00 (lifetime $857664.0) | match |
| R2 award `CONT_AWD_36C10B25N00070012_3600_36C10B25D0007_3600` | 036 | 2026 | 1 tx, $3,574,924.60 | 1 tx, $3,574,924.60 (lifetime $6809604.28) | match |
| R2 award `CONT_AWD_75F40124F19002_7524_75F40123A00031_7524` | 075 | 2024 | 1 tx, $24,547.95 | 1 tx, $24,547.95 (lifetime $196688.15) | match |
| R2 award `CONT_AWD_70RSAT24FC0000004_7001_70RTAC24A00000001_7001` | 070 | 2024 | 1 tx, $239,713.79 | 1 tx, $239,713.79 (lifetime $239713.79) | match |
| R2 award `CONT_AWD_2032H522F00425_2050_TIRNO17Z00027_2050` | 020 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $3967726.11) | match |
| R2 award `CONT_AWD_70CDCR18P00000129_7012_-NONE-_-NONE-` | 070 | 2024 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $8211.58) | match |
| R2 award `CONT_AWD_2032H524F00107_2050_2032H524A00003_2050` | 020 | 2024 | 3 tx, $4,897,165.72 | 3 tx, $4,897,165.72 (lifetime $4897165.72) | match |
| R2 award `CONT_AWD_2032H523F00539_2050_NNG15SC71B_8000` | 020 | 2023 | 1 tx, $65,318.25 | 1 tx, $65,318.25 (lifetime $65318.25) | match |
| R2 award `CONT_AWD_1331L523P13500039_1301_-NONE-_-NONE-` | 013 | 2026 | 1 tx, $-0.12 | 1 tx, $-0.12 (lifetime $4316285.88) | match |
| R2 award `CONT_AWD_36C10B22F0346_3600_47QTCA21D005U_4732` | 036 | 2026 | 1 tx, $-8,000.86 | 1 tx, $-8,000.86 (lifetime $1001267.33) | match |
| R2 award `CONT_AWD_75P00121F80030_7570_GS00Q12NSD0010_4732` | 075 | 2022 | 5 tx, $7,825,374.43 | 5 tx, $7,825,374.43 (lifetime $27478434.5) | match |
| R2 award `CONT_AWD_75H70522F06002_7527_75H70521D00001_7527` | 075 | 2022 | 1 tx, $104,000.00 | 1 tx, $104,000.00 (lifetime $70921.5) | match |
| R2 award `CONT_AWD_36C10B22F0041_3600_NNG15SD38B_8000` | 036 | 2025 | 1 tx, $203,224.26 | 1 tx, $203,224.26 (lifetime $1006162.63) | match |
| R2 award `CONT_AWD_HSBP1017C00137_7014_-NONE-_-NONE-` | 070 | 2024 | 2 tx, $-1,273,743.03 | 2 tx, $-1,273,743.03 (lifetime $370125532.06) | match |
| R2 award `CONT_AWD_2032L226F00006_2050_2032H524A00003_2050` | 020 | 2026 | 2 tx, $6,546.88 | 2 tx, $6,546.88 (lifetime $6546.88) | match |
| R2 award `CONT_AWD_75H70620P00466_7527_-NONE-_-NONE-` | 075 | 2022 | 1 tx, $-982.00 | 1 tx, $-982.00 (lifetime $12110.0) | match |
| R2 award `CONT_AWD_75ACF121F80006_7590_GS35F290CA_4732` | 075 | 2023 | 1 tx, $1,374,380.36 | 1 tx, $1,374,380.36 (lifetime $3983311.33) | match |
| R3 agency-year | 013 | 2022 | $1,173,544,861.68 | $1,173,544,861.68 | 0.00 |
| R3 agency-year | 013 | 2023 | $1,315,663,689.24 | $1,315,663,689.24 | 0.00 |
| R3 agency-year | 013 | 2024 | $1,387,577,676.82 | $1,387,577,676.82 | 0.00 |
| R3 agency-year | 013 | 2025 | $1,358,090,856.19 | $1,358,090,856.19 | 0.00 |
| R3 agency-year | 013 | 2026 | $1,640,571,963.90 | $1,640,571,963.90 | 0.00 |
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
| R3 agency-year | 036 | 2023 | $6,198,413,946.61 | $6,198,413,946.61 | 0.00 |
| R3 agency-year | 036 | 2024 | $6,872,839,324.71 | $6,872,839,324.71 | 0.00 |
| R3 agency-year | 036 | 2025 | $7,219,772,841.09 | $7,219,772,841.09 | 0.00 |
| R3 agency-year | 036 | 2026 | $8,597,084,338.79 | $8,597,084,338.79 | 0.00 |
| R3 agency-year | 070 | 2022 | $3,776,449,747.57 | $3,776,449,747.57 | 0.00 |
| R3 agency-year | 070 | 2023 | $4,146,356,227.22 | $4,146,356,227.22 | 0.00 |
| R3 agency-year | 070 | 2024 | $4,582,246,262.80 | $4,582,246,262.80 | 0.00 |
| R3 agency-year | 070 | 2025 | $4,596,020,513.99 | $4,596,020,513.99 | 0.00 |
| R3 agency-year | 070 | 2026 | $5,821,535,548.18 | $5,821,535,548.18 | 0.00 |
| R3 agency-year | 075 | 2022 | $5,518,703,581.60 | $5,518,703,581.60 | 0.00 |
| R3 agency-year | 075 | 2023 | $5,455,504,166.39 | $5,455,504,166.39 | 0.00 |
| R3 agency-year | 075 | 2024 | $5,513,022,707.43 | $5,513,022,707.43 | 0.00 |
| R3 agency-year | 075 | 2025 | $5,208,060,796.89 | $5,208,060,796.89 | 0.00 |
| R3 agency-year | 075 | 2026 | $5,697,146,007.06 | $5,697,146,007.06 | 0.00 |
