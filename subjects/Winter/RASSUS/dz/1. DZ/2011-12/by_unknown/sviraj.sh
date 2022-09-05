# Iduće će raditi samo ukoliko je datoteka zaista ovih karakteristika.
# Izmijenite parametre tako da odgovaraju onima datoteci.
aplay --file-type=raw --format=S16_LE --channels=2 --rate=44100 $1
