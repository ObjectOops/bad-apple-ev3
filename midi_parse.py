import pretty_midi

midi_data = pretty_midi.PrettyMIDI("assets/audio/alstroemeria_records_bad_apple.mid")

instrument_count = len(midi_data.instruments)

for i in range(instrument_count):
    instrument = midi_data.instruments[i]
    with open(f"assets/audio/raw/instrument_{i}.txt", "w+") as raw_out:
        for note in instrument.notes:
            raw_out.write(f"{note.pitch} {note.velocity} {note.get_duration()} {note.start} {note.end}\n")
