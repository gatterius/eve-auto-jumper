from AutoJumper import AutoJumper


dest_colors = [
    [163, 164, 15], [156, 157, 8],  # ansiblex non-pressed, citadel non-pressed
    [165, 166, 17], [159, 160, 11],  # ansiblex pressed, citadel pressed
    [164, 164, 11], [156, 156, 2],  # stargate non-pressed
    [166, 166, 13],  # stargate pressed, station non-pressed
    [160, 160, 6],  # stargate pressed, station pressed
]

AJ = AutoJumper(dest_colors=dest_colors, start_timeout=0.5)
AJ.choose_area()
AJ.find_dest_gate()

