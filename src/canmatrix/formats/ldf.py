from __future__ import absolute_import

import ldfparser
import canmatrix

def load(f, **options):  # type: (typing.IO, **typing.Any) -> canmatrix.CanMatrix
    ldf = ldfparser.parseLDF(path=f.name)  # using f.name is not nice, but works
    db = canmatrix.CanMatrix()

    for lin_frame in ldf.frames:
        cm_frame = canmatrix.Frame()
        cm_frame.name = lin_frame.name
        cm_frame.arbitration_id = cm_frame.arbitration_id.from_compound_integer(lin_frame.frame_id)
        cm_frame.add_transmitter(lin_frame.publisher.name)
        cm_frame.size = lin_frame.length

        for mapping in lin_frame.signal_map:
            lin_signal = mapping[1]
            cm_signal = canmatrix.Signal()
            cm_signal.name = lin_signal.name
            cm_signal.size = lin_signal.width
            cm_signal.initial_value = lin_signal.init_value
            for subscriber in lin_signal.subscribers:
                cm_signal.add_receiver(subscriber.name)
            cm_signal.start_bit = mapping[0]
            cm_frame.add_signal(cm_signal)
        db.add_frame(cm_frame)
    return db
