# Reconciliation against USAspending — 2026-10-26T17:05:46+00:00

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
| R1 count | 020 | 2026 | 2,859 | 2865 | -6 |
| R1 count | 028 | 2022 | 438 | 438 | 0 |
| R1 count | 028 | 2023 | 378 | 378 | 0 |
| R1 count | 028 | 2024 | 369 | 369 | 0 |
| R1 count | 028 | 2025 | 313 | 313 | 0 |
| R1 count | 028 | 2026 | 235 | 235 | 0 |
| R1 count | 036 | 2022 | 5,197 | 5197 | 0 |
| R1 count | 036 | 2023 | 4,270 | 4270 | 0 |
| R1 count | 036 | 2024 | 3,974 | 3974 | 0 |
| R1 count | 036 | 2025 | 3,919 | 3919 | 0 |
| R1 count | 036 | 2026 | 4,385 | 4385 | 0 |
| R1 count | 070 | 2022 | 8,020 | 8020 | 0 |
| R1 count | 070 | 2023 | 6,654 | 6654 | 0 |
| R1 count | 070 | 2024 | 5,502 | 5502 | 0 |
| R1 count | 070 | 2025 | 5,040 | 5040 | 0 |
| R1 count | 070 | 2026 | 4,449 | 4449 | 0 |
| R1 count | 075 | 2022 | 5,944 | 5944 | 0 |
| R1 count | 075 | 2023 | 5,465 | 5465 | 0 |
| R1 count | 075 | 2024 | 4,841 | 4841 | 0 |
| R1 count | 075 | 2025 | 4,310 | 4310 | 0 |
| R1 count | 075 | 2026 | 3,743 | 3743 | 0 |
| R2 award `CONT_AWD_75F40124F19023_7524_75F40120D00005_7524` | 075 | 2024 | 2 tx, $5,115,507.71 | 2 tx, $5,115,507.71 (lifetime $10158922.92) | match |
| R2 award `CONT_AWD_70FB7022F00000118_7022_70FB7019D00000011_7022` | 070 | 2022 | 1 tx, $18,912.50 | 1 tx, $18,912.50 (lifetime $0.0) | match |
| R2 award `CONT_AWD_70SBUR24F00000287_7003_HSHQDC12D00013_7001` | 070 | 2024 | 1 tx, $382,275.00 | 1 tx, $382,275.00 (lifetime $382275.0) | match |
| R2 award `CONT_AWD_75A50224F62009_7505_75A50222A00002_7505` | 075 | 2026 | 1 tx, $-1,092.52 | 1 tx, $-1,092.52 (lifetime $371.92) | match |
| R2 award `CONT_AWD_70T02022F7554N003_7013_NNG15SD02B_8000` | 070 | 2026 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $691304.4) | match |
| R2 award `CONT_AWD_1305M322PNWWN0538_1330_-NONE-_-NONE-` | 013 | 2022 | 1 tx, $9,461.24 | 1 tx, $9,461.24 (lifetime $9461.24) | match |
| R2 award `CONT_AWD_2032H318C00011_2001_-NONE-_-NONE-` | 020 | 2025 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $589404.01) | match |
| R2 award `CONT_AWD_36C26123F0028_3600_NNG15SD22B_8000` | 036 | 2026 | 1 tx, $8,238.35 | 1 tx, $8,238.35 (lifetime $32953.4) | match |
| R2 award `CONT_AWD_1331L523P13420146_1301_-NONE-_-NONE-` | 013 | 2026 | 2 tx, $525,321.04 | 2 tx, $525,321.04 (lifetime $3601554.64) | match |
| R2 award `CONT_AWD_36C10M25F50102_3600_NNG15SD38B_8000` | 036 | 2025 | 1 tx, $106,300.78 | 1 tx, $106,300.78 (lifetime $106300.78) | match |
| R2 award `CONT_AWD_HHSM500201300146C_7530_-NONE-_-NONE-` | 075 | 2024 | 2 tx, $-208,726.31 | 2 tx, $-208,726.31 (lifetime $2810736.15) | match |
| R2 award `CONT_AWD_205AE925C00048_2050_-NONE-_-NONE-` | 020 | 2025 | 1 tx, $124,084.74 | 1 tx, $124,084.74 (lifetime $124084.74) | match |
| R2 award `CONT_AWD_205AE922F00062_2050_NNG15SD13B_8000` | 020 | 2024 | 1 tx, $29,964.33 | 1 tx, $29,964.33 (lifetime $87310.21) | match |
| R2 award `CONT_AWD_2031JW22F00020_2046_2031JW21A00002_2046` | 020 | 2022 | 1 tx, $522,670.40 | 1 tx, $522,670.40 (lifetime $1853941.15) | match |
| R2 award `CONT_AWD_70FA3126F00000065_7022_47QTCB21D0332_4732` | 070 | 2026 | 1 tx, $3,451,680.00 | 1 tx, $3,451,680.00 (lifetime $3451680.0) | match |
| R2 award `CONT_AWD_28321321FDX030096_2800_47QTCA18D0081_4732` | 028 | 2026 | 2 tx, $838,406.40 | 2 tx, $838,406.40 (lifetime $8858784.0) | match |
| R2 award `CONT_AWD_1332KP25F0022_1330_1305M421ANAAA0054_1330` | 013 | 2025 | 2 tx, $603,844.80 | 2 tx, $603,844.80 (lifetime $1218687.2) | match |
| R2 award `CONT_AWD_75R60224F34057_7526_75R60221D00003_7526` | 075 | 2024 | 3 tx, $823,200.00 | 3 tx, $823,200.00 (lifetime $845075.0) | match |
| R2 award `CONT_AWD_36C10B23F0161_3600_NNG15SD27B_8000` | 036 | 2024 | 1 tx, $231,386.16 | 1 tx, $231,386.16 (lifetime $471759.36) | match |
| R2 award `CONT_AWD_36C24423F0319_3600_GS02F0106Y_4732` | 036 | 2026 | 1 tx, $11,450.61 | 1 tx, $11,450.61 (lifetime $44472.84) | match |
| R2 award `CONT_AWD_36C10A22F0139_3600_GS00T07NSD0007_4735` | 036 | 2024 | 1 tx, $-1,615.28 | 1 tx, $-1,615.28 (lifetime $323521.26) | match |
| R2 award `CONT_AWD_70RDAD21FR0000036_7001_70RTAC20D00000002_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $226707.78) | match |
| R2 award `CONT_AWD_VA11816F1338_3600_NNG15SD19B_8000` | 036 | 2022 | 2 tx, $13,407.63 | 2 tx, $13,407.63 (lifetime $383637.13) | match |
| R2 award `CONT_AWD_HHSN273201700014U_7529_GS00Q13NSA3000_4732` | 075 | 2023 | 1 tx, $-2,264.88 | 1 tx, $-2,264.88 (lifetime $181023.37) | match |
| R2 award `CONT_AWD_75N98020F00380_7529_GS06F1217Z_4732` | 075 | 2023 | 1 tx, $386,640.84 | 1 tx, $386,640.84 (lifetime $1526187.68) | match |
| R2 award `CONT_AWD_70B06C22F00001005_7014_47QTCA20D00CN_4732` | 070 | 2025 | 8 tx, $2,028,723.80 | 8 tx, $2,028,723.80 (lifetime $11919454.87) | match |
| R2 award `CONT_AWD_2099AC26F00038_2099_2099AC26D00002_2099` | 020 | 2026 | 1 tx, $332,641.05 | 1 tx, $332,641.05 (lifetime $332641.05) | match |
| R2 award `CONT_AWD_36C10B23F0044_3600_NNG15SD39B_8000` | 036 | 2023 | 1 tx, $293,328.00 | 1 tx, $293,328.00 (lifetime $293328.0) | match |
| R2 award `CONT_AWD_HHSP233201700293W_7570_NNG15SC85B_8000` | 075 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $206144.0) | match |
| R2 award `CONT_AWD_36C25921N0089_3600_36C25920A0065_3600` | 036 | 2023 | 1 tx, $41,338.80 | 1 tx, $41,338.80 (lifetime $204757.6) | match |
| R2 award `CONT_AWD_28321323FA0010144_2800_28321319A00040013_2800` | 028 | 2023 | 1 tx, $3,832,420.52 | 1 tx, $3,832,420.52 (lifetime $3832420.52) | match |
| R2 award `CONT_AWD_75040120F80003_7504_GS06F1233Z_4732` | 075 | 2022 | 1 tx, $878,988.80 | 1 tx, $878,988.80 (lifetime $2614495.0) | match |
| R2 award `CONT_AWD_75F40119F19006_7524_HHSF223201400024B_7524` | 075 | 2022 | 1 tx, $-88,429.79 | 1 tx, $-88,429.79 (lifetime $2168391.63) | match |
| R2 award `CONT_AWD_HHSD2002004034090030_7523_HHSD200200403409I_7523` | 075 | 2023 | 1 tx, $-83,957.33 | 1 tx, $-83,957.33 (lifetime $386995.14) | match |
| R2 award `CONT_AWD_70FA5022F00000082_7022_70FA5021D00000001_7022` | 070 | 2024 | 3 tx, $721,033.00 | 3 tx, $721,033.00 (lifetime $6319133.73) | match |
| R2 award `CONT_AWD_1332KP22FNEEG0047_1330_1305M421ANAAA0038_1330` | 013 | 2023 | 3 tx, $12,936,468.89 | 3 tx, $12,936,468.89 (lifetime $47473936.1) | match |
| R2 award `CONT_AWD_1305M425F0064_1330_1305M421GNAAJ0002_1330` | 013 | 2025 | 1 tx, $5,573,924.66 | 1 tx, $5,573,924.66 (lifetime $5573924.66) | match |
| R2 award `CONT_AWD_2032H520F00608_2050_GS35F0481Y_4732` | 020 | 2022 | 1 tx, $-2,636,754.00 | 1 tx, $-2,636,754.00 (lifetime $0.0) | match |
| R2 award `CONT_AWD_70FBR422F00000114_7022_70FA3018D00000002_7022` | 070 | 2022 | 1 tx, $138.87 | 1 tx, $138.87 (lifetime $135.69) | match |
| R2 award `CONT_AWD_70B02C20F00000830_7014_70B04C20A00000015_7014` | 070 | 2023 | 1 tx, $-621.98 | 1 tx, $-621.98 (lifetime $19893.31) | match |
| R2 award `CONT_AWD_75H71223F80114_7527_GS35F389DA_4732` | 075 | 2023 | 1 tx, $23,873.40 | 1 tx, $23,873.40 (lifetime $110206.16) | match |
| R2 award `CONT_AWD_70FBR923F00000043_7022_70FA3018D00000003_7022` | 070 | 2023 | 2 tx, $285.80 | 2 tx, $285.80 (lifetime $285.8) | match |
| R2 award `CONT_AWD_HSFE4017F0057_7022_GS35F0404K_4730` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $140424.0) | match |
| R2 award `CONT_AWD_7571TE26F80059_7571_47QTCA24D008A_4732` | 075 | 2026 | 1 tx, $79,530.00 | 1 tx, $79,530.00 (lifetime $79530.0) | match |
| R2 award `CONT_AWD_2032H521F00264_2050_47QTCA18D0081_4732` | 020 | 2022 | 1 tx, $985,958.73 | 1 tx, $985,958.73 (lifetime $4972726.44) | match |
| R2 award `CONT_AWD_HHSM500T0002_7530_HHSM500201300011I_7530` | 075 | 2023 | 2 tx, $28,350,837.00 | 2 tx, $28,350,837.00 (lifetime $253766656.22) | match |
| R2 award `CONT_AWD_75N98C25F00013_7529_GS35F025DA_4732` | 075 | 2025 | 2 tx, $12,376.80 | 2 tx, $12,376.80 (lifetime $12376.8) | match |
| R2 award `CONT_AWD_1331L523F13500645_1301_1331L523A13ES0051_1301` | 013 | 2023 | 1 tx, $57,876.00 | 1 tx, $57,876.00 (lifetime $57876.0) | match |
| R2 award `CONT_AWD_70FA3124F00000060_7022_NNG15SC73B_8000` | 070 | 2024 | 1 tx, $177,049.86 | 1 tx, $177,049.86 (lifetime $265574.79) | match |
| R2 award `CONT_AWD_2032H523F00764_2050_2032H523A00031_2050` | 020 | 2025 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $813553.93) | match |
| R3 agency-year | 013 | 2022 | $1,170,880,572.20 | $1,170,880,572.20 | 0.00 |
| R3 agency-year | 013 | 2023 | $1,314,026,936.94 | $1,314,026,936.94 | 0.00 |
| R3 agency-year | 013 | 2024 | $1,376,640,938.61 | $1,376,640,938.61 | 0.00 |
| R3 agency-year | 013 | 2025 | $1,354,182,418.21 | $1,354,182,418.21 | 0.00 |
| R3 agency-year | 013 | 2026 | $1,640,191,267.90 | $1,640,191,267.90 | 0.00 |
| R3 agency-year | 020 | 2022 | $1,819,975,487.12 | $1,819,975,487.12 | 0.00 |
| R3 agency-year | 020 | 2023 | $2,243,192,310.47 | $2,243,255,482.39 | -63,171.92 (row count short — see R1) |
| R3 agency-year | 020 | 2024 | $2,675,734,665.92 | $2,675,856,879.12 | -122,213.20 (row count short — see R1) |
| R3 agency-year | 020 | 2025 | $3,190,617,744.96 | $3,190,699,459.36 | -81,714.40 (row count short — see R1) |
| R3 agency-year | 020 | 2026 | $2,291,020,438.39 | $2,291,010,893.67 | 9,544.72 (row count short — see R1) |
| R3 agency-year | 028 | 2022 | $1,004,831,340.74 | $1,004,831,340.74 | 0.00 |
| R3 agency-year | 028 | 2023 | $1,052,732,490.79 | $1,052,732,490.79 | 0.00 |
| R3 agency-year | 028 | 2024 | $938,381,084.59 | $938,381,084.59 | 0.00 |
| R3 agency-year | 028 | 2025 | $781,780,087.36 | $781,780,087.36 | 0.00 |
| R3 agency-year | 028 | 2026 | $1,057,911,411.10 | $1,057,911,411.10 | 0.00 |
| R3 agency-year | 036 | 2022 | $6,730,049,177.23 | $6,730,049,177.23 | 0.00 |
| R3 agency-year | 036 | 2023 | $6,198,741,321.22 | $6,198,741,321.22 | 0.00 |
| R3 agency-year | 036 | 2024 | $6,873,105,668.98 | $6,873,105,668.98 | 0.00 |
| R3 agency-year | 036 | 2025 | $7,218,679,612.82 | $7,218,679,612.82 | 0.00 |
| R3 agency-year | 036 | 2026 | $8,594,554,065.61 | $8,594,554,065.61 | 0.00 |
| R3 agency-year | 070 | 2022 | $3,776,449,747.57 | $3,776,449,747.57 | 0.00 |
| R3 agency-year | 070 | 2023 | $4,149,874,995.92 | $4,149,874,995.92 | 0.00 |
| R3 agency-year | 070 | 2024 | $4,580,168,576.98 | $4,580,168,576.98 | 0.00 |
| R3 agency-year | 070 | 2025 | $4,594,614,260.48 | $4,594,614,260.48 | 0.00 |
| R3 agency-year | 070 | 2026 | $5,809,614,689.42 | $5,809,614,689.42 | 0.00 |
| R3 agency-year | 075 | 2022 | $5,518,703,581.60 | $5,518,703,581.60 | 0.00 |
| R3 agency-year | 075 | 2023 | $5,455,504,166.39 | $5,455,504,166.39 | 0.00 |
| R3 agency-year | 075 | 2024 | $5,513,153,072.97 | $5,513,153,072.97 | 0.00 |
| R3 agency-year | 075 | 2025 | $5,208,060,799.64 | $5,208,060,799.64 | 0.00 |
| R3 agency-year | 075 | 2026 | $5,697,146,007.06 | $5,697,146,007.06 | 0.00 |
