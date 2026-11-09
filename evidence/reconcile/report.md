# Reconciliation against USAspending — 2026-11-09T20:40:53+00:00

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
| R1 count | 036 | 2024 | 3,970 | 3970 | 0 |
| R1 count | 036 | 2025 | 3,917 | 3917 | 0 |
| R1 count | 036 | 2026 | 4,380 | 4380 | 0 |
| R1 count | 070 | 2022 | 8,020 | 8020 | 0 |
| R1 count | 070 | 2023 | 6,654 | 6654 | 0 |
| R1 count | 070 | 2024 | 5,502 | 5502 | 0 |
| R1 count | 070 | 2025 | 5,042 | 5042 | 0 |
| R1 count | 070 | 2026 | 4,451 | 4451 | 0 |
| R1 count | 075 | 2022 | 5,944 | 5944 | 0 |
| R1 count | 075 | 2023 | 5,465 | 5465 | 0 |
| R1 count | 075 | 2024 | 4,842 | 4842 | 0 |
| R1 count | 075 | 2025 | 4,310 | 4310 | 0 |
| R1 count | 075 | 2026 | 3,743 | 3743 | 0 |
| R2 award `CONT_AWD_205AE925F00048_2050_NNG15SC71B_8000` | 020 | 2025 | 2 tx, $1,410,885.96 | 2 tx, $1,410,885.96 (lifetime $2962860.54) | match |
| R2 award `CONT_AWD_75H71123P00083_7527_-NONE-_-NONE-` | 075 | 2024 | 1 tx, $8,016.00 | 1 tx, $8,016.00 (lifetime $9312.0) | match |
| R2 award `CONT_AWD_2031ZB22F00073_2041_47QTCB21D0306_4732` | 020 | 2023 | 1 tx, $2,127,044.28 | 1 tx, $2,127,044.28 (lifetime $4466216.85) | match |
| R2 award `CONT_AWD_36C10B22F0031_3600_NNG15SD24B_8000` | 036 | 2022 | 2 tx, $158,315.82 | 2 tx, $158,315.82 (lifetime $1463620.8) | match |
| R2 award `CONT_AWD_2032H518F01270_2050_NNG15SD20B_8000` | 020 | 2023 | 1 tx, $-7,151.85 | 1 tx, $-7,151.85 (lifetime $54814.37) | match |
| R2 award `CONT_AWD_75FCMC22F0067_7530_GS35F711GA_4732` | 075 | 2025 | 1 tx, $7,033,162.22 | 1 tx, $7,033,162.22 (lifetime $33977538.4) | match |
| R2 award `CONT_AWD_75N97022F00001_7529_HHSN316201500050W_7529` | 075 | 2022 | 1 tx, $629,617.91 | 1 tx, $629,617.91 (lifetime $629617.91) | match |
| R2 award `CONT_AWD_75F40122C00157_7524_-NONE-_-NONE-` | 075 | 2023 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $3703521.6) | match |
| R2 award `CONT_AWD_HHSD2002010371980009_7523_HHSD200201037198I_7523` | 075 | 2025 | 2 tx, $0.00 | 2 tx, $0.00 (lifetime $84957884.56) | match |
| R2 award `CONT_AWD_70Z04423FC2PL0015_7008_70Z04423DC2PL0001_7008` | 070 | 2026 | 1 tx, $39,200.00 | 1 tx, $39,200.00 (lifetime $147199.84) | match |
| R2 award `CONT_AWD_70B04C23F00001213_7014_NNG15SD11B_8000` | 070 | 2023 | 1 tx, $809,800.00 | 1 tx, $809,800.00 (lifetime $809800.0) | match |
| R2 award `CONT_AWD_1331L523FNCNP0663_1301_1331L523A13ES0021_1301` | 013 | 2023 | 1 tx, $22,913.40 | 1 tx, $22,913.40 (lifetime $24089.4) | match |
| R2 award `CONT_AWD_HSCG3207FR00006_7008_GS35F0852N_4730` | 070 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $89565.32) | match |
| R2 award `CONT_AWD_70B04C24F00000184_7014_47QTCK18D0001_4732` | 070 | 2026 | 8 tx, $32,300,080.87 | 8 tx, $32,300,080.87 (lifetime $110881128.98) | match |
| R2 award `CONT_AWD_75H70722F80132_7527_HHSN316201200018W_7529` | 075 | 2022 | 1 tx, $54,163.62 | 1 tx, $54,163.62 (lifetime $51898.78) | match |
| R2 award `CONT_AWD_2032H521F00869_2050_TIRNO17Z00027_2050` | 020 | 2024 | 2 tx, $-3,203.25 | 2 tx, $-3,203.25 (lifetime $9961200.17) | match |
| R2 award `CONT_AWD_HSCETE11J00470_7012_HSHQDC07D00029_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $7046.08) | match |
| R2 award `CONT_AWD_VA26016P1607_3600_-NONE-_-NONE-` | 036 | 2022 | 1 tx, $-11,095.44 | 1 tx, $-11,095.44 (lifetime $43505.01) | match |
| R2 award `CONT_AWD_36C10A22P0008_3600_-NONE-_-NONE-` | 036 | 2026 | 2 tx, $45,467.21 | 2 tx, $45,467.21 (lifetime $208053.78) | match |
| R2 award `CONT_AWD_75F40123P00099_7524_-NONE-_-NONE-` | 075 | 2023 | 1 tx, $98,317.00 | 1 tx, $98,317.00 (lifetime $314222.0) | match |
| R2 award `CONT_AWD_1305M322FNWWW0091_1330_1305M421ANAAA0080_1330` | 013 | 2025 | 1 tx, $182,823.28 | 1 tx, $182,823.28 (lifetime $876625.08) | match |
| R2 award `CONT_AWD_36C26023F0187_3600_GS07F187GA_4732` | 036 | 2023 | 1 tx, $11,817.60 | 1 tx, $11,817.60 (lifetime $23989.6) | match |
| R2 award `CONT_AWD_36C24524F0127_3600_47QTCA20D00B5_4732` | 036 | 2025 | 1 tx, $-675.00 | 1 tx, $-675.00 (lifetime $0.0) | match |
| R2 award `CONT_AWD_75N95023F00001_7529_HHSN316201200110W_7529` | 075 | 2024 | 1 tx, $3,714,658.07 | 1 tx, $3,714,658.07 (lifetime $11649300.48) | match |
| R2 award `CONT_AWD_DOCRA133W17CC0023_1330_DOCSA130114BU0005_1301` | 013 | 2023 | 1 tx, $-12,001.16 | 1 tx, $-12,001.16 (lifetime $230219.27) | match |
| R2 award `CONT_AWD_HHSM500201400225C_7530_-NONE-_-NONE-` | 075 | 2023 | 1 tx, $-34,682.95 | 1 tx, $-34,682.95 (lifetime $2452722.05) | match |
| R2 award `CONT_AWD_70RDA125FR0000025_7001_NNG15SC78B_8000` | 070 | 2025 | 2 tx, $3,707,054.60 | 2 tx, $3,707,054.60 (lifetime $6195992.07) | match |
| R2 award `CONT_AWD_75FCMC21F0003_7530_HHSM500201600067I_7530` | 075 | 2024 | 1 tx, $789,339.00 | 1 tx, $789,339.00 (lifetime $3780690.0) | match |
| R2 award `CONT_AWD_36C25623P1376_3600_-NONE-_-NONE-` | 036 | 2025 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $214001.0) | match |
| R2 award `CONT_AWD_70CMSD26P00000140_7012_-NONE-_-NONE-` | 070 | 2026 | 1 tx, $1,690,000.00 | 1 tx, $1,690,000.00 (lifetime $1690000.0) | match |
| R2 award `CONT_AWD_HSCETE11J00279_7012_HSHQDC07D00030_7001` | 070 | 2022 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $4465.04) | match |
| R2 award `CONT_AWD_75F40120F80622_7524_NNG15SD19B_8000` | 075 | 2024 | 1 tx, $8,314.20 | 1 tx, $8,314.20 (lifetime $39441.6) | match |
| R2 award `CONT_AWD_1333LB22F00000177_1323_NNG15SC65B_8000` | 013 | 2022 | 1 tx, $226,561.85 | 1 tx, $226,561.85 (lifetime $226561.85) | match |
| R2 award `CONT_AWD_2032H520F00484_2050_NNG15SC71B_8000` | 020 | 2024 | 1 tx, $18,600.00 | 1 tx, $18,600.00 (lifetime $74400.0) | match |
| R2 award `CONT_AWD_28321320P00050275_2800_-NONE-_-NONE-` | 028 | 2025 | 2 tx, $675,819.00 | 2 tx, $675,819.00 (lifetime $3313210.96) | match |
| R2 award `CONT_AWD_36C10B24F0253_3600_NNG15SD22B_8000` | 036 | 2026 | 2 tx, $8,294,900.00 | 2 tx, $8,294,900.00 (lifetime $27027030.0) | match |
| R2 award `CONT_AWD_70RDA124FR0000038_7001_70RTAC21D00000006_7001` | 070 | 2025 | 2 tx, $184,518.12 | 2 tx, $184,518.12 (lifetime $434915.68) | match |
| R2 award `CONT_AWD_36C10B21C0017_3600_-NONE-_-NONE-` | 036 | 2022 | 1 tx, $246,000.00 | 1 tx, $246,000.00 (lifetime $1106880.0) | match |
| R2 award `CONT_AWD_36C10A22F0143_3600_NNG15SD22B_8000` | 036 | 2026 | 2 tx, $2,327,240.00 | 2 tx, $2,327,240.00 (lifetime $40514680.0) | match |
| R2 award `CONT_AWD_36C77620P0019_3600_-NONE-_-NONE-` | 036 | 2024 | 1 tx, $42,267.00 | 1 tx, $42,267.00 (lifetime $183450.0) | match |
| R2 award `CONT_AWD_75F40123F80401_7524_75N98119D00034_7529` | 075 | 2026 | 1 tx, $2,592,141.40 | 1 tx, $2,592,141.40 (lifetime $9706823.63) | match |
| R2 award `CONT_AWD_36C10B25F0082_3600_NNG15SD42B_8000` | 036 | 2026 | 1 tx, $-21,474.80 | 1 tx, $-21,474.80 (lifetime $11124.0) | match |
| R2 award `CONT_AWD_VA69D17C0230_3600_-NONE-_-NONE-` | 036 | 2023 | 2 tx, $-19,403.62 | 2 tx, $-19,403.62 (lifetime $432076.87) | match |
| R2 award `CONT_AWD_75P00122F80084_7570_GS35F0095W_4730` | 075 | 2023 | 3 tx, $73,510.77 | 3 tx, $73,510.77 (lifetime $923481.75) | match |
| R2 award `CONT_AWD_75F40120F19006_7524_75F40118A10050_7524` | 075 | 2023 | 1 tx, $-11,541.69 | 1 tx, $-11,541.69 (lifetime $6968964.44) | match |
| R2 award `CONT_AWD_HHSM500201700041C_7530_-NONE-_-NONE-` | 075 | 2025 | 1 tx, $-34,987.88 | 1 tx, $-34,987.88 (lifetime $1667222.05) | match |
| R2 award `CONT_AWD_36C10B23C0032_3600_-NONE-_-NONE-` | 036 | 2024 | 1 tx, $0.00 | 1 tx, $0.00 (lifetime $375443.44) | match |
| R2 award `CONT_AWD_HSTS0317JCT6017_7013_HSHQDC13DE2023_7001` | 070 | 2022 | 1 tx, $-5,581.91 | 1 tx, $-5,581.91 (lifetime $434712.49) | match |
| R2 award `CONT_AWD_7571TE26F80126_7571_47QTCA24A0002_4732` | 075 | 2026 | 1 tx, $273,158.07 | 1 tx, $273,158.07 (lifetime $273158.07) | match |
| R2 award `CONT_AWD_205AE925F00211_2050_2032H523A00029_2050` | 020 | 2025 | 1 tx, $65,520.00 | 1 tx, $65,520.00 (lifetime $65520.0) | match |
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
| R3 agency-year | 036 | 2024 | $6,872,937,775.67 | $6,872,937,775.67 | 0.00 |
| R3 agency-year | 036 | 2025 | $7,218,604,432.11 | $7,218,604,432.11 | 0.00 |
| R3 agency-year | 036 | 2026 | $8,594,020,370.51 | $8,594,020,370.51 | 0.00 |
| R3 agency-year | 070 | 2022 | $3,776,449,747.57 | $3,776,449,747.57 | 0.00 |
| R3 agency-year | 070 | 2023 | $4,149,874,995.92 | $4,149,874,995.92 | 0.00 |
| R3 agency-year | 070 | 2024 | $4,580,168,576.98 | $4,580,168,576.98 | 0.00 |
| R3 agency-year | 070 | 2025 | $4,594,607,687.63 | $4,594,607,687.63 | 0.00 |
| R3 agency-year | 070 | 2026 | $5,811,659,583.53 | $5,811,659,583.53 | 0.00 |
| R3 agency-year | 075 | 2022 | $5,518,703,581.60 | $5,518,703,581.60 | 0.00 |
| R3 agency-year | 075 | 2023 | $5,455,504,166.39 | $5,455,504,166.39 | 0.00 |
| R3 agency-year | 075 | 2024 | $5,513,022,707.43 | $5,513,022,707.43 | 0.00 |
| R3 agency-year | 075 | 2025 | $5,208,060,799.64 | $5,208,060,799.64 | 0.00 |
| R3 agency-year | 075 | 2026 | $5,697,146,007.06 | $5,697,146,007.06 | 0.00 |
