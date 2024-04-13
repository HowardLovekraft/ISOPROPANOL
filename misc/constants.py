constants = {
    "create_table_query":
    """
        CREATE TABLE IF NOT EXISTS isopropanol (
            id BIGINT,
            health INT,
            inventory INT[8]
            
        )
    """,
    "ammo_types": {
        "blank": "O",
        "live": "I"
    },
    "items": ("BEER", "MAGNIFIER", "HANDSAW", "CIGARETTES", "PILLS",
              "PHONE", "ADRENALINE", "INVENTOR", "HANDCUFFS")
}