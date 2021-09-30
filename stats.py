def show_stats(frame_count, net_error_count, scheme_error_count, all_schemes, check_not_crc, vrc_not_crc, uncaught, burst):
    print(f'\nError injected in {net_error_count} frames out of {frame_count}')
    print(f'Noise percentage : {net_error_count * 100 / frame_count}%')
    print(f'Average burst length : {burst/net_error_count}')

    print(f'\nError detection accuracy of VRC : {scheme_error_count[0]*100/net_error_count}')
    print(f'Error detection accuracy of LRC : {scheme_error_count[1]*100/net_error_count}')
    print(f'Error detection accuracy of Checksum : {scheme_error_count[2] * 100 / net_error_count}')
    print(f'Error detection accuracy of CRC : {scheme_error_count[3] * 100 / net_error_count}')

    print('\nSample error uncaught by VRC : ')
    print(f'Original dataword : {uncaught[0][0][0][:32]}')
    print(f'Original codeword : {uncaught[0][0][0]}')
    print(f'Injected codeword : {uncaught[0][1][1]}')

    print('\nSample error uncaught by LRC : ')
    print(f'Original dataword : {uncaught[1][0][0][:32]}')
    print(f'Original codeword : {uncaught[1][0][0]}')
    print(f'Injected codeword : {uncaught[1][1][1]}')

    print('\nSample error uncaught by Checksum : ')
    print(f'Original dataword : {uncaught[2][0][0][:32]}')
    print(f'Original codeword : {uncaught[2][0][0]}')
    print(f'Injected codeword : {uncaught[2][1][1]}')

    print('\nSample error uncaught by CRC : ')
    print(f'Original dataword : {uncaught[3][0][0][:32]}')
    print(f'Original codeword : {uncaught[3][0][0]}')
    print(f'Injected codeword : {uncaught[3][1][1]}')

    print(f'\nErrors detected by all four schemes : {len(all_schemes)}')
    print(f'Occurrence : {len(all_schemes)*100/net_error_count}%')
    if len(all_schemes) != 0:
        print(f'Original dataword : {all_schemes[0][0][:32]}')
        print(f'Original codeword : {all_schemes[0][0]}')
        print(f'Injected codeword : {all_schemes[0][1]}')

    print(f'\nErrors detected by checksum but not by CRC : {len(check_not_crc)}')
    print(f'Occurrence : {len(check_not_crc) * 100 / net_error_count}%')
    if len(check_not_crc) != 0:
        print(f'Original dataword : {all_schemes[0][0][:32]}')
        print(f'Original codeword : {check_not_crc[0][0]}')
        print(f'Injected codeword : {check_not_crc[0][1]}')

    print(f'\nErrors detected by VRC but not by CRC : {len(vrc_not_crc)}')
    print(f'Occurrence : {len(vrc_not_crc) * 100 / net_error_count}%')
    if len(vrc_not_crc) != 0:
        print(f'Original dataword : {all_schemes[0][0][:32]}')
        print(f'Original codeword : {vrc_not_crc[0][0]}')
        print(f'Injected codeword : {vrc_not_crc[0][1]}')